#!/usr/bin/env bash
#
# Remove render intermediates and OS junk. Safe to run anytime; prints every
# path it removes and does nothing on a second run.
#
#     ./clean.sh          # junk only: .DS_Store, AppleDouble files, *.pid,
#                         # Office lock files, Rplots*.pdf, *.quarto_ipynb,
#                         # stray root-level *_files/ dirs
#     ./clean.sh --deep   # also every regenerable render: _book/, _freeze/,
#                         # and .quarto/ caches (lists in targets.conf)
#     ./clean.sh --scratch [days]
#                         # report working/ by size and age, flag loose files,
#                         # and OFFER to move task dirs untouched for [days]
#                         # (default 14) into archived_materials/. Interactive;
#                         # moves only on a per-entry yes, never deletes.
#
# Never touches data/ (fetched working copy) or archived_materials/; working/
# only via --scratch, above.
set -euo pipefail

cd "$(dirname "$0")"

# Shared preamble, for targets_section (the --deep lists live in targets.conf).
. tools/lib/preamble.sh

deep=false; scratch=false; scratch_days=14
case "${1:-}" in
  --deep) deep=true ;;
  --scratch)
    scratch=true
    if [ "${2:-}" != "" ]; then scratch_days=$2; fi ;;
  "") ;;
  -h|--help) sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
  *) echo "ERROR: unknown option '$1' (valid: --deep, --scratch [days])" >&2; exit 1 ;;
esac

# --- Scratch review: working/ is scratch, but it composts without attention --
if [ "$scratch" = true ]; then
  now=$(date +%s)
  echo ">> working/ contents (idle = days since newest file inside changed):"
  loose=()
  candidates=()
  for e in working/* ; do
    [ -e "$e" ] || continue
    name=${e#working/}
    [ "$name" = "README.md" ] && continue
    newest=$(find "$e" -type f -exec stat -f %m {} + 2>/dev/null | sort -rn | head -1)
    [ -z "$newest" ] && newest=$(stat -f %m "$e")   # empty dir: its own mtime
    idle=$(( (now - newest) / 86400 ))
    size=$(du -sh "$e" 2>/dev/null | cut -f1)
    printf "  %8s  %3sd idle  %s\n" "$size" "$idle" "$name"
    if [ -f "$e" ]; then
      loose+=("$e")
    elif [ -d "$e" ] && [ "$idle" -ge "$scratch_days" ]; then
      candidates+=("$e")
    fi
  done
  if [ ${#loose[@]} -gt 0 ]; then
    echo
    echo ">> ${#loose[@]} loose file(s) at working/ root -- the convention is one"
    echo "   directory per task. File them or archive them:"
    printf '     %s\n' "${loose[@]}"
  fi
  if [ ${#candidates[@]} -eq 0 ]; then
    echo ">> No task dirs idle ${scratch_days}+ days. Nothing to archive."
    exit 0
  fi
  echo
  echo ">> Task dirs idle ${scratch_days}+ days. Move to archived_materials/working_archive/?"
  mkdir -p archived_materials/working_archive
  for d in "${candidates[@]}"; do
    printf "   move %s? [y/N] " "$d"
    read -r ans
    if [ "$ans" = "y" ]; then
      mv "$d" archived_materials/working_archive/
      echo "   -> archived_materials/working_archive/${d#working/}"
    fi
  done
  exit 0
fi

# Print-and-remove helper; skips paths that don't exist so reruns are quiet.
removed=0
remove() {
  for path in "$@"; do
    [ -e "$path" ] || continue
    echo "  rm $path"
    rm -rf "$path"
    removed=$((removed + 1))
  done
}

echo ">> Cleaning junk..."

# OS/editor droppings and render strays, wherever they landed (except .git,
# the fetched data working copy, and the hands-off scratch/archive dirs).
while IFS= read -r f; do
  remove "$f"
done < <(find . \( -path ./.git -o -path ./data -o -path ./working \
                   -o -path ./archived_materials \) -prune -o \
              \( -name '.DS_Store' -o -name '._*' -o -name '*.pid' \
                 -o -name '~$*' -o -name 'Rplots*.pdf' \
                 -o -name '*.quarto_ipynb' \) -type f -print)

# Stray render-artifact dirs at the repo root (a standalone render dropped
# them next to the source).
for d in ./*_files; do
  [ -d "$d" ] || continue
  remove "$d"
done

# Regenerable outputs that land at the repo root: knitr's default figure/ dir
# and one-off render dirs.
remove figure output tmp out

if [ "$deep" = true ]; then
  echo ">> Cleaning regenerable renders (--deep)..."
  # Both lists are declared in targets.conf; ** globs mean any depth.
  while IFS= read -r d; do
    remove "$d"
  done < <(targets_section render-dirs)
  while IFS= read -r g; do
    case "$g" in
      *'**'*)
        root=${g%%/\*\**}; name=${g##*/}
        while IFS= read -r f; do
          remove "$f"
        done < <(find "$root" -name "$name" -type f -print 2>/dev/null) ;;
      *)
        # shellcheck disable=SC2086  # unquoted so the shell expands the glob
        remove $g ;;
    esac
  done < <(targets_section render-globs)
fi

echo ">> Done ($removed removed)."
