#!/usr/bin/env bash
#
# One command from edited source to published, verified book site.
#
#     ./ship.sh                    # auto: build what changed, deploy, verify
#     ./ship.sh --only regression_01_intro.qmd     # explicit single chapter
#     ./ship.sh --full             # rebuild everything
#     ./ship.sh --detect-only      # print what auto mode would do, then stop
#     ./ship.sh --rollback-site    # undo the last site deploy
#
# Auto mode diffs the working tree + commits against the source sha recorded
# in the last deploy (gh-pages commit message), maps changed files to build
# targets via targets.conf, and runs exactly those. Every run ends with a
# ledger saying what happened stage by stage.
set -uo pipefail   # NOT -e: stages handle their own failures for the ledger

cd "$(dirname "$0")"

# Shared preamble: SITE_CLONE/SITE_URL local config + UTF-8 locale pinning.
. tools/lib/preamble.sh

# --- Flags -------------------------------------------------------------------
mode=auto            # auto | explicit | rollback
build_flags=()
detect_only=false

while [ "$#" -gt 0 ]; do
  case "$1" in
    --full)          mode=explicit; build_flags=() ;;
    --only)          mode=explicit; shift; build_flags+=(--only "$1") ;;
    --rollback-site) mode=rollback ;;
    --detect-only)   detect_only=true ;;
    -h|--help)       sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "ERROR: unknown option '$1'." >&2; exit 1 ;;
  esac
  shift
done

# --- Ledger ------------------------------------------------------------------
ledger_names=(); ledger_states=(); ledger_notes=()
note() { ledger_names+=("$1"); ledger_states+=("$2"); ledger_notes+=("${3:-}"); }

print_ledger() {
  echo
  echo "== ship ledger =============================================="
  local i
  for i in "${!ledger_names[@]}"; do
    printf "  %-12s %-8s %s\n" "${ledger_names[$i]}" "${ledger_states[$i]}" "${ledger_notes[$i]}"
  done
  echo "============================================================="
}

fail_out() {   # <stage> <note> -- record, print ledger, exit 1
  note "$1" "FAILED" "$2"
  print_ledger
  exit 1
}

# --- Rollback ----------------------------------------------------------------
if [ "$mode" = rollback ]; then
  if [ ! -d "$SITE_CLONE/.git" ]; then
    echo "ERROR: no site clone at $SITE_CLONE." >&2; exit 1
  fi
  git -C "$SITE_CLONE" fetch origin gh-pages
  git -C "$SITE_CLONE" reset --hard origin/gh-pages --quiet
  last=$(git -C "$SITE_CLONE" log -1 --format=%s)
  case "$last" in
    "publish: "*) ;;
    *) echo "ERROR: last gh-pages commit is not a deploy ('$last'); not reverting." >&2
       exit 1 ;;
  esac
  echo ">> Reverting deploy: $last"
  git -C "$SITE_CLONE" revert --no-edit HEAD || exit 1
  git -C "$SITE_CLONE" push origin gh-pages || {
    echo "ERROR: push failed; retry with './publish.sh --deploy-only'." >&2; exit 1; }
  echo ">> Site rolled back."
  exit 0
fi

# --- Auto-detect targets -----------------------------------------------------
if [ "$mode" = auto ]; then
  deployed_sha=""
  if [ -d "$SITE_CLONE/.git" ]; then
    git -C "$SITE_CLONE" fetch origin gh-pages 2>/dev/null
    subj=$(git -C "$SITE_CLONE" log origin/gh-pages -1 --format=%s 2>/dev/null || true)
    case "$subj" in
      "publish: "*) deployed_sha=$(printf '%s' "$subj" | awk '{print $2}' | sed 's/+dirty//') ;;
    esac
  fi

  if [ -z "$deployed_sha" ] || ! git rev-parse --verify -q "$deployed_sha" >/dev/null; then
    echo ">> No usable deploy record on gh-pages; running a full build."
    mode=explicit; build_flags=()
  else
    # Everything different from what's deployed: commits since + working tree.
    # -uall expands untracked directories into their files; without it a new
    # directory arrives as a bare "dir/" that mis-classifies.
    changed=$( { git diff --name-only "$deployed_sha" HEAD 2>/dev/null;
                 git status --porcelain -uall | awk '{print $NF}'; } | sort -u )

    build_book=false
    only_targets=()
    unmapped=()

    # Classification is declared in targets.conf ([classify]): shell-glob
    # pattern -> target, first match wins.
    classify_pats=(); classify_tgts=()
    while read -r pat tgt; do
      classify_pats+=("$pat"); classify_tgts+=("$tgt")
    done < <(targets_section classify)
    if [ ${#classify_pats[@]} -eq 0 ]; then
      echo "ERROR: no [classify] section found in targets.conf." >&2; exit 1
    fi

    classify() {
      local f=$1 i
      for i in "${!classify_pats[@]}"; do
        # shellcheck disable=SC2053
        if [[ $f == ${classify_pats[$i]} ]]; then
          printf '%s\n' "${classify_tgts[$i]}"; return
        fi
      done
      printf 'unmapped\n'
    }

    while IFS= read -r f; do
      [ -n "$f" ] || continue
      target=$(classify "$f")
      case "$target" in
        none)        ;;
        book)        build_book=true ;;
        chapter)     only_targets+=("$f") ;;
        unmapped)    unmapped+=("$f") ;;
        *) echo "ERROR: targets.conf maps '$f' to unknown target '$target'." >&2
           exit 1 ;;
      esac
    done <<< "$changed"

    if [ ${#unmapped[@]} -gt 0 ]; then
      echo "ERROR: changed files with no matching [classify] pattern in targets.conf:" >&2
      printf '  %s\n' "${unmapped[@]}" >&2
      echo "Add a pattern there, or run with explicit flags (--full/--only)." >&2
      exit 1
    fi

    build_flags=()
    if [ "$build_book" = false ]; then
      for f in ${only_targets[@]+"${only_targets[@]}"}; do
        build_flags+=(--only "$f")
      done
    fi

    if [ "$build_book" = false ] && [ ${#build_flags[@]} -eq 0 ]; then
      echo ">> Nothing changed since the last deploy ($deployed_sha)."
      note "detect" "done" "no changes since $deployed_sha"
      skip_build=true
    else
      [ "$build_book" = true ] && build_flags=()
      echo ">> Auto-detected build: ${build_flags[*]:-full}"
      note "detect" "done" "targets: ${build_flags[*]:-full}"
      skip_build=false
    fi
  fi
fi
[ "${skip_build:-}" = "" ] && skip_build=false
if [ "$mode" = explicit ]; then
  note "detect" "done" "explicit: ${build_flags[*]:-full}"
fi

if [ "$detect_only" = true ]; then
  echo ">> --detect-only: stopping before any build."
  print_ledger
  exit 0
fi

# --- Stage: house terms -------------------------------------------------------
# The PostToolUse hook only sees Claude's edits; hand edits in Positron reach
# the site unchecked unless we sweep here. Warn-only: terminology drift is a
# content bug to fix and re-ship, not a reason to hold a deploy.
if terms_out=$(./tools/checks/check_terms.sh --all 2>&1); then
  note "terms" "done" ""
else
  printf '%s\n' "$terms_out"
  note "terms" "WARNED" "drift found (above); fix with ./tools/checks/check_terms.sh --fix"
fi

# --- Stage: number consistency ------------------------------------------------
# Source-side companion to the rounded-arithmetic check below. That one reads
# the deployed pages and can only see numbers that survive as text; this one
# reads the .qmd, so it sees the ones that end up inside a figure.
if numbers_out=$(./tools/checks/check_number_consistency.R --all 2>&1); then
  note "numbers" "done" "no quantity displayed at two precisions"
else
  printf '%s\n' "$numbers_out"
  note "numbers" "WARNED" "precision drift (above); adjudicate or record in tools/number_consistency_ignore.tsv"
fi

# --- Stage: review-history consistency ----------------------------------------
# Declined-edit logs and the coverage registry are public content in this repo
# and must stay keyed to real chapter sources.
if rh_out=$(./tools/check_review_history.sh 2>&1); then
  note "reviewhist" "done" ""
else
  printf '%s\n' "$rh_out"
  note "reviewhist" "WARNED" "review-history inconsistency (above)"
fi

# --- Stage: build + deploy (publish.sh does both) ----------------------------
if [ "$skip_build" = true ]; then
  note "build" "skipped" "nothing to rebuild"
  note "deploy" "skipped" ""
else
  if ./publish.sh ${build_flags[@]+"${build_flags[@]}"}; then
    note "build" "done" ""
    note "deploy" "done" ""
  else
    fail_out "build+deploy" "see errors above; site NOT updated"
  fi

  # --- Stage: live verify ----------------------------------------------------
  # Existence (HEAD 200) is not enough: after a typo fix the URL existed
  # before, and the CDN can serve stale bytes. So byte-compare the HTML files
  # this deploy changed against the clone, retrying through Pages' deploy lag.
  # SHIP_SITE_URL override exists for testing against a local server.
  site_url="${SHIP_SITE_URL:-$SITE_URL}"
  changed_html=$(git -C "$SITE_CLONE" show --name-only --format= HEAD 2>/dev/null |
                 grep '\.html$' | head -10 || true)

  if [ -z "$changed_html" ]; then
    note "verify" "skipped" "no HTML changed in this deploy"
  else
    verify_fail=""
    for rel in $changed_html; do
      ok=false
      for attempt in 1 2 3; do
        if curl -sf -H 'Cache-Control: no-cache' -o /tmp/ship_verify.$$ \
             "$site_url/$rel" 2>/dev/null &&
           cmp -s /tmp/ship_verify.$$ "$SITE_CLONE/$rel"; then
          ok=true; break
        fi
        sleep $((attempt * 15))   # ride out GitHub Pages deploy latency
      done
      if [ "$ok" = false ]; then verify_fail="$verify_fail $site_url/$rel"; fi
    done
    rm -f /tmp/ship_verify.$$
    if [ -n "$verify_fail" ]; then
      note "verify" "FAILED" "stale or unreachable:$verify_fail"
      echo "WARNING: the site may not have finished deploying; the URLs above" >&2
      echo "         do not yet serve the new content. Check in a minute." >&2
    else
      note "verify" "done" "$(printf '%s\n' "$changed_html" | wc -l | tr -d ' ') file(s) byte-verified live"
    fi
  fi

  # --- Stage: rounded-arithmetic check ---------------------------------------
  # Re-do every explicit arithmetic statement on the changed pages using the
  # numbers a reader can actually see. A hit is a content bug, not a deploy
  # bug: warn loudly, don't block.
  if [ -z "$changed_html" ]; then
    note "arith" "skipped" "no HTML changed in this deploy"
  else
    arith_files=()
    for rel in $changed_html; do
      [ -f "$SITE_CLONE/$rel" ] && arith_files+=("$SITE_CLONE/$rel")
    done
    if [ ${#arith_files[@]} -eq 0 ]; then
      note "arith" "skipped" "changed HTML not present in site clone"
    elif Rscript tools/checks/check_rounded_arithmetic.R "${arith_files[@]}"; then
      note "arith" "done" "displayed-value arithmetic closes on all changed pages"
    else
      note "arith" "FAILED" "a page prints arithmetic its displayed numbers contradict"
      echo "WARNING: a deployed page states arithmetic that fails when redone with" >&2
      echo "         the rounded numbers it displays (details above). Fix the" >&2
      echo "         source -- usually round-then-compute -- and re-ship." >&2
    fi
  fi

  # --- Stage: cross-repo link sweep ------------------------------------------
  # The book links to the webapps site (and other external pages); a page move
  # there 404s with zero signal here. curl HEAD every distinct absolute link
  # to our sibling sites found in the deployed HTML this run touched -- and
  # always the three app link pages, whose whole content is the link.
  link_pages="sap_sampling_app.html sap_bootstrap_app.html bagging_app.html"
  sweep_files=""
  for rel in $changed_html $link_pages; do
    [ -f "$SITE_CLONE/$rel" ] && sweep_files="$sweep_files $SITE_CLONE/$rel"
  done
  if [ -z "${sweep_files// /}" ]; then
    note "links" "skipped" "no pages to sweep"
  else
    # shellcheck disable=SC2086
    links=$(grep -hoE 'https://[a-z.]*github\.io/(stats-webapps|teaching-data)[^"#]*' \
              $sweep_files 2>/dev/null | sort -u || true)
    if [ -z "$links" ]; then
      note "links" "done" "no cross-repo links on swept pages"
    else
      dead=""
      for u in $links; do
        curl -sf -o /dev/null -I "$u" || dead="$dead $u"
      done
      if [ -n "$dead" ]; then
        note "links" "FAILED" "dead cross-repo link(s):$dead"
        echo "WARNING: cross-repo links above do not resolve; fix the target or" >&2
        echo "         the link and re-ship." >&2
      else
        note "links" "done" "$(printf '%s\n' "$links" | wc -l | tr -d ' ') cross-repo link(s) alive"
      fi
    fi
  fi
fi

# --- Reminders ---------------------------------------------------------------
print_ledger
if [ -d "$SITE_CLONE/.git" ]; then
  last_full=$(git -C "$SITE_CLONE" log --format='%s %ct' | awk '/ book / {print $NF; exit}')
  if [ -n "$last_full" ] && [ $(( $(date +%s) - last_full )) -gt $((14 * 86400)) ]; then
    echo ">> Note: no full book render deployed in 14+ days; nav/search may be"
    echo "   drifting -- consider './ship.sh --full' when convenient."
  fi
fi

exit 0
