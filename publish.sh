#!/usr/bin/env bash
#
# Build the book and deploy it to GitHub Pages (the gh-pages branch).
#
#     ./publish.sh                 # full book render and deploy
#     ./publish.sh --only regression_01_intro.qmd   # exactly one chapter
#     ./publish.sh --deploy-only   # push a deploy that failed on the network
#     ./publish.sh --no-deploy     # build/stage only, skip the deploy
#     ./publish.sh --squash-site-history   # compress gh-pages history (prompts)
#
# Deploys COMPOSE onto the published site rather than replacing it: a local
# clone of gh-pages (outside the repo) is reset to origin, only what this run
# rebuilt is copied in, and the result is committed and pushed. A single-file
# run never needs a prior full build on this machine -- the pulled site
# supplies everything else -- and two machines can alternate freely. Every
# deploy is a git commit in the clone: its log is the deploy history.
#
# This repo is the SOLE writer to its gh-pages branch: the book is the whole
# site, so a full render composes with a plain --delete rsync and no scope
# blacklist.
set -euo pipefail

cd "$(dirname "$0")"

# Shared preamble: SITE_CLONE/SITE_URL local config + UTF-8 locale pinning.
. tools/lib/preamble.sh

# --- Parse flags -------------------------------------------------------------
do_book=false
deploy=true; deploy_only=false; squash=false
only_files=()

if [ "$#" -eq 0 ]; then
  do_book=true
else
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --book)       do_book=true ;;   # accepted for muscle memory; same as no args
      --only)       shift; only_files+=("$1") ;;
      --deploy-only) deploy_only=true ;;
      --no-deploy)  deploy=false ;;
      --squash-site-history) squash=true ;;
      -h|--help)
        sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//'
        exit 0 ;;
      *)
        echo "ERROR: unknown option '$1'." >&2
        echo "Valid: --only <chapter.qmd> --deploy-only --no-deploy --squash-site-history" >&2
        exit 1 ;;
    esac
    shift
  done
  # --only alone means "just those chapters"; otherwise default to full book.
  if [ ${#only_files[@]} -eq 0 ] && [ "$deploy_only" = false ] && \
     [ "$squash" = false ]; then
    do_book=true
  fi
fi

# --- Locate quarto -----------------------------------------------------------
# Prefer a quarto on PATH; otherwise fall back to the copy bundled inside an
# IDE. Positron comes first: it's the editor this project standardizes on, and
# it ships a newer Quarto than RStudio does, so a fallback build here matches
# what an interactive render in Positron produces. Mismatched bundles show up
# as pointless churn -- the same chapter rebuilt under two Quarto versions
# differs in its generator string and asset hashes even when the prose is
# identical.
if ! command -v quarto >/dev/null 2>&1; then
  for ide_quarto in \
    "/Applications/Positron.app/Contents/Resources/app/quarto/bin" \
    "$HOME/Applications/Positron.app/Contents/Resources/app/quarto/bin" \
    "/Applications/RStudio.app/Contents/Resources/app/quarto/bin"
  do
    if [ -x "$ide_quarto/quarto" ]; then
      export PATH="$ide_quarto:$PATH"
      break
    fi
  done
fi
if ! command -v quarto >/dev/null 2>&1; then
  echo "ERROR: quarto not found on PATH, or bundled in Positron.app/RStudio.app." >&2
  echo "Install Quarto (https://quarto.org) or open Positron at least once." >&2
  exit 1
fi

# --- Site clone preflight ----------------------------------------------------
# The deploy target is a single-branch clone of gh-pages OUTSIDE the repo with
# its own .git. First-deploy bootstrap: a fresh repo has no gh-pages branch
# yet, so create it as an orphan and push it up before the normal flow.
clone_preflight() {
  local url
  # SITE_REMOTE override exists for testing the deploy machinery against a
  # local bare repo without touching the real site.
  url="${SITE_REMOTE:-$(git remote get-url origin)}"
  if [ ! -d "$SITE_CLONE/.git" ]; then
    echo ">> Creating site clone at $SITE_CLONE (first run on this machine)..."
    mkdir -p "$(dirname "$SITE_CLONE")"
    if ! git clone --branch gh-pages --single-branch "$url" "$SITE_CLONE" 2>/dev/null; then
      echo ">> No gh-pages branch on the remote yet; bootstrapping it."
      git clone --no-checkout "$url" "$SITE_CLONE"
      git -C "$SITE_CLONE" checkout --orphan gh-pages
      git -C "$SITE_CLONE" rm -rf --quiet . 2>/dev/null || true
      git -C "$SITE_CLONE" clean -fdq
      git -C "$SITE_CLONE" commit --allow-empty --quiet -m "init gh-pages"
      git -C "$SITE_CLONE" push -u origin gh-pages
    fi
  fi
  # Start every deploy from the published state -- the other machine's work.
  # The clone is disposable output, never a merge site: hard reset, and sweep
  # untracked leftovers from any aborted previous compose.
  if ! git -C "$SITE_CLONE" fetch origin gh-pages; then
    echo "ERROR: cannot reach the site remote (network? auth?). The site was" >&2
    echo "       NOT updated; re-run this command when the connection is back." >&2
    exit 1
  fi
  git -C "$SITE_CLONE" reset --hard origin/gh-pages --quiet
  git -C "$SITE_CLONE" clean -fdq
}

# --- Squash site history (maintenance) ---------------------------------------
# Every deploy is a commit, so gh-pages history grows with use. This rewrites
# the branch to a single commit holding the current site. Destructive to
# remote history by design, hence the prompt.
if [ "$squash" = true ]; then
  clone_preflight
  count=$(git -C "$SITE_CLONE" rev-list --count HEAD)
  echo ">> gh-pages currently has $count deploy commit(s)."
  printf "Squash to a single commit and force-push? [y/N] "
  read -r ans
  if [ "$ans" != "y" ]; then echo ">> Aborted."; exit 0; fi
  new=$(git -C "$SITE_CLONE" commit-tree 'HEAD^{tree}' \
        -m "site history squashed $(date -u '+%Y-%m-%d %H:%MZ') (was $count commits)")
  git -C "$SITE_CLONE" reset --hard "$new" --quiet
  git -C "$SITE_CLONE" push --force origin gh-pages
  echo ">> Done. gh-pages is now 1 commit."
  exit 0
fi

# --- Deploy-only: retry a push that failed on the network --------------------
if [ "$deploy_only" = true ]; then
  if [ ! -d "$SITE_CLONE/.git" ]; then
    echo "ERROR: no site clone at $SITE_CLONE; nothing pending to push." >&2
    exit 1
  fi
  echo ">> Pushing pending deploy from $SITE_CLONE..."
  git -C "$SITE_CLONE" push origin gh-pages
  echo ">> Done."
  exit 0
fi

# ==============================================================================
# BUILD -- render the requested pieces into _book/ (scratch, per-run)
# ==============================================================================

targets=""

# --- Cross-reference safety for single-chapter renders ------------------------
# A single-file render is safe for prose fixes: quarto resolves references to
# other chapters from the cached index in .quarto/xref. Two hazards remain,
# each checked at the right moment:
#
# (1) The cache must exist, or the render itself emits unresolved "?@fig-..."
#     references. Checked here, before rendering.
# (2) The edit must not change the chapter's own numbering (adding or removing
#     a numbered figure/table/section): other chapters' references to those
#     numbers go stale on the live site with no warning. Checked at deploy
#     time by comparing numbering extracted from the DEPLOYED chapter HTML
#     (the clone's copy) against the freshly rendered one -- deliberately not
#     against local caches, which the render itself rewrites; a cache-based
#     check passes on the second attempt and the bad publish slips through.
xref_cache_ok() {
  python3 - "$1" <<'EOF'
import json, os, sys
qmd = sys.argv[1]
idx_path = ".quarto/xref/INDEX"
if not os.path.exists(idx_path):
    print("no"); sys.exit(0)
idx = json.load(open(idx_path))
print("yes" if qmd in idx else "no")
EOF
}

# The numbering fingerprint of a rendered chapter: its crossref anchor ids,
# the header section numbers, and the rendered Figure/Table numbers. Any
# change to these is a change other chapters could be referencing.
html_numbering() {
  python3 - "$1" <<'EOF'
import re, sys
html = open(sys.argv[1], encoding="utf-8", errors="replace").read()
# Authored anchor ids only. Quarto also emits derived ids carrying a
# per-render UUID (fig-x-caption-<uuid>); including those would flag every
# render as a numbering change.
ids = sorted(set(i for i in
                 re.findall(r'id="((?:fig|tbl|sec|thm|def|exm|eq)-[^"]+)"', html)
                 if "-caption-" not in i))
secs = sorted(re.findall(r'class="header-section-number">([^<]+)<', html))
nums = sorted(re.findall(r'(?:Figure|Table)(?:&nbsp;|\s)([0-9A-Z][0-9A-Z.]*)', html))
print("|".join(ids) + "##" + "|".join(secs) + "##" + "|".join(nums))
EOF
}

# --- Build each --only chapter ------------------------------------------------
only_composed=()
for f in ${only_files[@]+"${only_files[@]}"}; do
  case "$f" in
    */*)
      echo "ERROR: --only takes book chapters (*.qmd at the repo root); got '$f'." >&2
      exit 1
      ;;
    *.qmd)
      stem=$(basename "$f" .qmd)
      if [ "$(xref_cache_ok "$f")" != "yes" ]; then
        echo "ERROR: no cached cross-reference index for $f on this machine." >&2
        echo "       One full './publish.sh' is needed first (new chapter, or" >&2
        echo "       .quarto/ was cleaned); single-file renders resolve" >&2
        echo "       cross-references from that cache." >&2
        exit 1
      fi
      echo ">> Rendering chapter $stem..."
      quarto render "$f"
      only_composed+=("$stem")
      targets="$targets $stem"
      ;;
    *)
      echo "ERROR: --only expects a .qmd file, got '$f'." >&2
      exit 1
      ;;
  esac
done

if [ "$do_book" = true ]; then
  echo ">> Rendering book..."
  quarto render
  targets="$targets book"
fi

if [ "$deploy" = false ]; then
  echo ">> Build staged in _book/ (deploy skipped by --no-deploy)."
  exit 0
fi

# ==============================================================================
# DEPLOY -- compose this run's output onto the published site and push
# ==============================================================================

clone_preflight

# Numbering drift check for --only chapters, against the DEPLOYED site (see
# the note at xref_cache_ok). Runs before anything is composed, so a block
# leaves the clone exactly as origin published it.
for stem in ${only_composed[@]+"${only_composed[@]}"}; do
  if [ ! -f "$SITE_CLONE/$stem.html" ]; then
    echo "ERROR: $stem.html is not on the published site yet; a new chapter" >&2
    echo "       needs a full './publish.sh' (navigation + numbering)." >&2
    exit 1
  fi
  old_num=$(html_numbering "$SITE_CLONE/$stem.html")
  new_num=$(html_numbering "_book/$stem.html")
  if [ "$old_num" != "$new_num" ]; then
    echo "ERROR: numbering in $stem changed relative to the published site" >&2
    echo "       (figures/tables/sections gained, lost, or renumbered)." >&2
    echo "       Other chapters' references to it would go stale, so this" >&2
    echo "       cannot ship alone -- run a full './publish.sh'." >&2
    exit 1
  fi
done

echo ">> Composing deploy..."

# Full build: the staged _book IS the whole site (this repo is the sole
# writer to gh-pages). `working` stays excluded on principle: scratch renders
# have ended up inside _book/ before, and scratch never ships.
if [ "$do_book" = true ]; then
  rsync -a --delete --exclude .git --exclude working _book/ "$SITE_CLONE"/
else
  # --only chapters: copy exactly those files' outputs.
  for stem in ${only_composed[@]+"${only_composed[@]}"}; do
    cp "_book/$stem.html" "$SITE_CLONE"/
    # The chapter's asset dir gets --delete: quarto hash-names figures, and
    # without it renamed assets accumulate in the site forever.
    if [ -d "_book/${stem}_files" ]; then
      rsync -a --delete "_book/${stem}_files/" "$SITE_CLONE/${stem}_files/"
    fi
    # Shared pieces a single-file render refreshes; additive, never --delete.
    [ -f _book/search.json ] && cp _book/search.json "$SITE_CLONE"/
    [ -d _book/site_libs ] && rsync -a _book/site_libs/ "$SITE_CLONE"/site_libs/
  done
fi

# Strip macOS Finder junk so a stray .DS_Store never ships.
find "$SITE_CLONE" -name '.DS_Store' -delete
rm -rf "$SITE_CLONE"/working

# --- Guards: run on the CLONE, i.e. on exactly what would be pushed -----------
# The book repo contains no solutions, but the guards are cheap and this site
# is public: keep them as defense in depth against anything that rode in via
# an include or a stray copy. On any failure the clone is reset, so bad
# content cannot ride a later deploy.
guard_fail() {
  echo "Aborting: resetting the site clone; nothing was pushed." >&2
  git -C "$SITE_CLONE" reset --hard origin/gh-pages --quiet
  git -C "$SITE_CLONE" clean -fdq
  exit 1
}

# Nothing over 100 MB may reach gh-pages.
if find "$SITE_CLONE" -path "$SITE_CLONE/.git" -prune -o -type f -size +100M -print | grep -q .; then
  echo "ERROR: file(s) exceed GitHub's 100 MB limit:" >&2
  find "$SITE_CLONE" -path "$SITE_CLONE/.git" -prune -o -type f -size +100M -exec du -h {} \; >&2
  guard_fail
fi

leaked=false
if find "$SITE_CLONE" -path "$SITE_CLONE/.git" -prune -o -iname '*solution*' -print | grep -q .; then
  echo "ERROR: staged file(s) with 'solution' in the name:" >&2
  find "$SITE_CLONE" -path "$SITE_CLONE/.git" -prune -o -iname '*solution*' -print >&2
  leaked=true
fi
if grep -rIl --exclude-dir=.git 'when-profile="solutions"' "$SITE_CLONE" >/dev/null 2>&1; then
  echo "ERROR: staged text file(s) contain problem-set solution markup:" >&2
  grep -rIl --exclude-dir=.git 'when-profile="solutions"' "$SITE_CLONE" >&2
  leaked=true
fi
if [ "$leaked" = true ]; then
  guard_fail
fi

# --- Commit and push ----------------------------------------------------------
git -C "$SITE_CLONE" add -A
if git -C "$SITE_CLONE" diff --cached --quiet; then
  echo ">> Site unchanged; nothing to deploy."
else
  src_sha=$(git rev-parse --short HEAD)
  dirty=""
  git diff --quiet && git diff --cached --quiet || dirty="+dirty"
  git -C "$SITE_CLONE" commit --quiet \
    -m "publish: ${src_sha}${dirty} $(hostname -s)$targets $(date -u '+%Y-%m-%d %H:%MZ')"
  echo ">> Pushing to GitHub Pages..."
  if ! git -C "$SITE_CLONE" push origin gh-pages; then
    echo "ERROR: push failed (network? auth?). The deploy commit is safe in" >&2
    echo "       $SITE_CLONE -- retry with './publish.sh --deploy-only'." >&2
    exit 1
  fi
  ndeploys=$(git -C "$SITE_CLONE" rev-list --count HEAD)
  if [ "$ndeploys" -gt 200 ]; then
    echo ">> Note: gh-pages has $ndeploys deploy commits; consider" \
         "'./publish.sh --squash-site-history'."
  fi
fi

# --- Tidy render intermediates ------------------------------------------------
if [ ${#only_files[@]} -eq 0 ]; then
  ./clean.sh
fi

echo ">> Done."
