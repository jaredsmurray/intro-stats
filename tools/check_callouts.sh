#!/usr/bin/env bash
set -euo pipefail

# The checks below use ripgrep; on a machine without it (fresh clone, CI),
# fall back to grep -E, which handles every pattern this script uses.
if ! command -v rg >/dev/null 2>&1; then
  rg() {
    if [ "$1" = -q ]; then shift; grep -qE "$@"; else grep -E "$@"; fi
  }
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fixture_source="$repo_root/tests/fixtures/callouts"
check_root="$(mktemp -d "${TMPDIR:-/tmp}/callout-check.XXXXXX")"

cleanup() {
  if [[ "${CALLOUT_CHECK_KEEP:-0}" == "1" ]]; then
    echo "Callout regression outputs retained at: $check_root"
    return
  fi
  if [[ -n "$check_root" && -d "$check_root" ]]; then
    rm -rf -- "$check_root"
  fi
}
trap cleanup EXIT

cp "$fixture_source/index.qmd" "$check_root/index.qmd"
cp "$fixture_source/chapter-two.qmd" "$check_root/chapter-two.qmd"
cp "$fixture_source/_quarto.yml" "$check_root/_quarto.yml"
cp "$fixture_source/_quarto-pdf-default.yml" "$check_root/_quarto-pdf-default.yml"
cp "$fixture_source/_quarto-full-formulas.yml" "$check_root/_quarto-full-formulas.yml"

mkdir -p "$check_root/styles" "$check_root/tex" "$check_root/_extensions"
cp "$repo_root/styles/callouts.css" "$check_root/styles/callouts.css"
cp "$repo_root/tex/callouts.tex" "$check_root/tex/callouts.tex"
cp -R "$repo_root/_extensions/custom-numbered-blocks" "$check_root/_extensions/"
cp -R "$repo_root/_extensions/details" "$check_root/_extensions/"

cd "$check_root"
quarto render
quarto render --profile pdf-default --to pdf
quarto render --profile full-formulas --to pdf

html_one="_output/html/index.html"
html_two="_output/html/chapter-two.html"
pdf_default="_output/pdf-default/callouts-default.pdf"
pdf_full="_output/pdf-full-formulas/callouts-full-formulas.pdf"

for output in "$html_one" "$html_two" "$pdf_default" "$pdf_full"; do
  test -f "$output"
done

# Static numbered blocks use icons rather than disclosure widgets.
rg -q 'Definition fobx-simplebox fobx-default fobx-static' "$html_one"
rg -q 'Notation fobx-simplebox fobx-default fobx-static' "$html_one"
rg -q 'Exercise fobx-simplebox fobx-default fobx-static' "$html_one"
! rg -q '<details class="(Definition|Notation|Exercise)' "$html_one"
rg -q '<details class="TechnicalDetail' "$html_one"
rg -q 'bi-book' "$html_one"
rg -q 'bi-braces' "$html_one"
rg -q 'bi-pencil-square' "$html_one"

# Formula and solution disclosures preserve semantic classes and labels.
rg -q 'class="formula-details"' "$html_one"
rg -q 'class="solution-details"' "$html_one"
rg -q '<summary>Details and formulas</summary>' "$html_one"
rg -q '<summary>Solution</summary>' "$html_one"

# Every custom counter restarts with the second chapter.
rg -q 'Definition 2\.1' "$html_two"
rg -q 'Exercise 2\.1' "$html_two"
rg -q 'Technical detail 2\.1' "$html_two"
pdftotext -layout "$pdf_default" - |
  rg -q 'Definition 2\.1: Standardized value'
pdftotext -layout "$pdf_default" - |
  rg -q 'Exercise 2\.1: Delivery-time z-score'
pdftotext -layout "$pdf_default" - |
  rg -q 'Technical detail 2\.1: Sampling variability'

# Default PDF omits ordinary formula detail, retains explicit overrides and
# solutions; the full-formula PDF includes the ordinary formula detail.
! pdftotext -layout "$pdf_default" - |
  rg -q 'The formula finds each value'
pdftotext -layout "$pdf_default" - |
  rg -q 'Formula included in the default PDF'
pdftotext -layout "$pdf_default" - |
  rg -q 'The sample standard deviation is measured in dollars'
pdftotext -layout "$pdf_full" - |
  rg -q 'The formula finds each value'

echo "Callout regression checks passed."
