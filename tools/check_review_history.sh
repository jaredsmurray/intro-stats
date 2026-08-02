#!/usr/bin/env bash
#
# check_review_history.sh -- book-specific consistency check for review_history/.
#
# Enforces the five rules that make the review memory trustworthy after a
# chapter rename or a new review:
#
#   1. each declined_edits/<name>.yml declares chapter_source <name>.qmd
#   2. each declared chapter_source exists as a root .qmd
#   3. entry ids are unique within a log
#   4. every coverage `source:` exists as a root .qmd, and every root chapter
#      listed in _quarto.yml (excluding index.qmd and the appendices) has a
#      coverage entry
#   5. every `evidence:` reference uses the frozen-tag form
#      sta380_2026@final-summer-2026:<path>
#
# Exit 0 on success, 1 on any failure. No arguments.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DECLINED="review_history/declined_edits"
COVERAGE="review_history/coverage.yml"
EVIDENCE_RE='^sta380_2026@final-summer-2026:[^[:space:]]+$'

fail=0
problem() { printf 'FAIL  %s\n' "$*" >&2; fail=1; }
note()    { printf '  %s\n' "$*"; }

[ -d "$DECLINED" ] || { problem "missing $DECLINED"; exit 1; }
[ -f "$COVERAGE" ] || { problem "missing $COVERAGE"; exit 1; }

# --- the book's root chapter sources, from _quarto.yml ----------------------
# Chapter entries between `chapters:` and `appendices:`, minus index.qmd.
chapters="$(awk '
  /^  appendices:/ { inbook = 0 }
  /^  chapters:/   { inbook = 1 }
  inbook && match($0, /[A-Za-z0-9_.-]+\.qmd/) {
    print substr($0, RSTART, RLENGTH)
  }
' _quarto.yml | grep -v '^index\.qmd$' | sort -u)"

[ -n "$chapters" ] || { problem "could not read the chapter list from _quarto.yml"; exit 1; }
nch=$(printf '%s\n' "$chapters" | wc -l | tr -d ' ')

# --- 1-3, 5: declined-edit logs ---------------------------------------------
nlogs=0
for log in "$DECLINED"/*.yml; do
  [ -e "$log" ] || break
  nlogs=$((nlogs + 1))
  base="$(basename "$log" .yml)"

  src="$(awk -F': *' '/^chapter_source:/ { print $2; exit }' "$log")"
  if [ -z "$src" ]; then
    problem "$log: no chapter_source declared"
    continue
  fi
  # 1. filename matches the declared source
  [ "$src" = "${base}.qmd" ] ||
    problem "$log: filename implies ${base}.qmd but chapter_source is $src"
  # 2. the source exists
  [ -f "$src" ] ||
    problem "$log: chapter_source $src does not exist as a root .qmd"

  # 3. ids unique within the log
  dupes="$(awk '/^  - id:/ { sub(/^  - id: */, ""); print }' "$log" |
           sort | uniq -d)"
  if [ -n "$dupes" ]; then
    problem "$log: duplicate entry ids"
    printf '%s\n' "$dupes" | while read -r d; do note "id: $d"; done
  fi
done
[ "$nlogs" -gt 0 ] || problem "$DECLINED contains no logs"

# 5. evidence reference format, across every log and the coverage registry
while IFS= read -r ref; do
  [ -n "$ref" ] || continue
  printf '%s' "$ref" | grep -Eq "$EVIDENCE_RE" ||
    problem "evidence reference is not a frozen-tag reference: $ref"
done <<EOF
$(awk '
  /^ *evidence:/ { inev = 1; next }
  inev && /^ *- / { sub(/^ *- */, ""); print; next }
  { inev = 0 }
' "$DECLINED"/*.yml)
EOF

# --- 4: coverage registry ----------------------------------------------------
covsrc="$(awk -F': *' '/^  - source:/ { print $2 }' "$COVERAGE" | sort -u)"
[ -n "$covsrc" ] || problem "$COVERAGE lists no sources"

while IFS= read -r s; do
  [ -n "$s" ] || continue
  [ -f "$s" ] || problem "$COVERAGE: source $s does not exist as a root .qmd"
done <<EOF
$covsrc
EOF

while IFS= read -r c; do
  [ -n "$c" ] || continue
  printf '%s\n' "$covsrc" | grep -qx "$c" ||
    problem "$COVERAGE: no coverage entry for chapter $c"
done <<EOF
$chapters
EOF

# --- report ------------------------------------------------------------------
if [ "$fail" -eq 0 ]; then
  printf 'review_history OK: %s declined-edit logs, %s coverage entries, %s chapters\n' \
    "$nlogs" "$(printf '%s\n' "$covsrc" | wc -l | tr -d ' ')" "$nch"
fi
exit "$fail"
