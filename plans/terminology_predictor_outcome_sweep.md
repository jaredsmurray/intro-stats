# Inspect the terminology ledger's predictor/outcome rows, then standardize book-wide

Opened 2026-07-29 from the chapter-19 batch adjudication. Jared: "add a todo
to inspect/update the register on outcomes and predictors and to standardize
terminology across the book."

## What prompted it

`tools/terminology_ledger.tsv` rows 35 and 36 name `regression_01_intro.qmd`
as `first_defined_in` for **predictor** and **outcome variable**. The ch. 19
audit proved that false: neither term was defined there and "outcome variable"
did not appear in the chapter at all.

Ch. 19's finding 8 fix has since been applied, so the attribution is now true
as of this date:

> Here $y_i$ is the **outcome variable**, the thing we predict --- sale price
> --- and $x_i$ is the **predictor**, living area.

That closes the falsity but not the question below.

## The two jobs

**1. ~~Inspect the rows~~ — INSPECTED 2026-07-30; row edits await Jared.**
Findings against current ch. 19 (post-finding-8 fix):

- **predictor** row: `first_defined_in` is now true (line 96 bolds the term).
  Symbol column says "X, x_i" — ch. 19 itself uses only $x_i$; capital $X$
  first appears in ch. 21's population model. Fine if the column describes
  unit-wide usage; flag if it must match the defining chapter.
- **outcome variable** row: `first_defined_in` true (same sentence). Bare
  "outcome" earns its allowed-variant status — ch. 19 uses it at lines 123,
  241, 591. "dependent variable" (near-miss): zero hits anywhere. Good.
- **adjusted comparison** row: attribution true — §"Multiple regression
  coefficients are adjusted comparisons" (line 367) with consistent reuse at
  400, 472, 504; line 515 uses "adjusts for"/"controls for" in quotes,
  matching the allowed variants.
- **Near-miss violations found in the unit** (evidence for job 2, not row
  changes): bare unattributed "covariate(s)" at `regression_05:443`,
  `regression_03:520`, `regression_06:300` (the ledger allows it only
  attributed to other books; `regression_02:183` does it right); "response"
  used ~7 times in `regression_06` (incl. a comment header and prose at 300,
  563, 574, 962) despite being a listed near-miss for outcome variable;
  `regression_05:443` also brushes the "effect of X" near-miss ("estimate the
  effect of one while adjusting for the other").

**2. Standardize across the book.** The rows were written as if one chapter
owned these terms; the regression unit is several chapters long and the
prediction chapters use the same vocabulary. Survey actual usage across
`regression_*.qmd`, `prediction_*.qmd`, the slide decks, the coding
supplements, and the problem sets, then pick one house form per concept and
sweep. Watch specifically for `response`, `dependent variable`, and
`explanatory variable` (already ledgered as near-misses) and for bare
`covariate`, which the ledger allows only when attributed to other books'
vocabulary.

Candidates promoted to a machine-checked rule belong in `style_terms.tsv` so
`tools/check_terms.sh` enforces them; note that neither "predictor" nor
"outcome variable" is currently in that file.

## Relationship to the wider ledger pass

This is a slice of D2 in `working/reconcile_student_review.md` (the ~80 held
ledger rows across waves 2–4). If that dedicated ledger session happens first,
fold this in rather than running it twice. The distinguishing piece here is
job 2 — the book-wide usage sweep and sweep-to-one-form, which D2 does not
cover.
