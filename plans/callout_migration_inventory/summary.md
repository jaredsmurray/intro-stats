# Whole-book callout sweep: high-level findings

## Coverage

The source-only sweep covers all 28 in-scope pages:

- the landing page;
- 25 substantive chapters;
- the dataset appendix and download page.

The three embedded app pages were excluded because they are tools rather than
expository chapters. No chapter source, prose, markup, or generated output was
changed.

Detailed inventories:

- `foundations.md` — landing page, single-variable, and two-variable chapters;
- `probability_inference.md` — probability and inference chapters;
- `regression_prediction.md` — regression, prediction, and appendices.

## Overall assessment

There are strong candidates for every callout type, but they should not all be
implemented in one pass. The sweep is an inventory of plausible uses, not a
recommendation to box every listed passage.

The cleanest early wins are:

1. migrate existing definition-style notes into numbered Definitions;
2. retain genuinely conceptual existing notes as native Key idea callouts;
3. use Warning/Common mistake only for a small number of chapter-specific
   failure modes;
4. use Technical detail selectively for algebra, derivations, and exact
   formulas that interrupt a conceptual explanation.

Notation is the sparsest category and should stay that way. It is most useful
when several related symbols form a system that students must retrieve later,
not for every symbol introduced in an equation.

## Strong recurring patterns

### Definitions

The best candidates are canonical, reusable concepts: density plots,
percentiles/quantiles, standard deviation, dummy variables, probability
models, random variables, distribution parameters, confidence intervals,
residuals, residual standard error, reference categories, interactions,
polynomial regression, and cross-validation.

Several chapters currently distribute a definition across an example, a
formula, and interpretive prose. Those need a local rewrite before the
numbered Definition can be concise and non-duplicative.

### Native callouts

- **Key idea** works best for chapter-organizing principles and conceptual
  bridges: how to describe a distribution, covariance/correlation rules,
  sampling-distribution logic, the CI/test connection, adjusted comparisons,
  diagnostic reasoning, and bias–variance.
- **Interpretation** is especially valuable when translating spread,
  covariance, regression predictions and coefficients, log-scale effects, and
  interval targets back into substantive language.
- **Warning/Common mistake** has many high-value uses: outlier deletion,
  confusing density height with probability, reversing conditional
  probabilities, treating zero correlation as independence, misreading
  confidence intervals and p-values, causal readings of regression, trusting
  extrapolation, interaction main effects, and test-data leakage.

Warnings should remain short and rare. When the source currently contains a
long list of limitations, retain the examples in normal prose and box only a
boundary that is especially salient in that chapter. Do not repeat a universal
warning every time it applies.

### Technical details and formula disclosure

Good candidates include:

- exact formulas for standard deviation and related summaries;
- density integrals and probability calculations;
- expectation/variance derivations;
- the finite-population-to-iid bridge and bootstrap rationale;
- the $R^2$ variance decomposition;
- plug-in predictive distributions;
- dummy-variable and interaction algebra;
- exact log-ratio conversions;
- the bias–variance decomposition.

These are often better implemented as formula details nested within a
Definition, Key idea, or Interpretation rather than as standalone numbered
Technical details.

### Exercises: deferred

The most natural initial exercises already exist as questions followed by
answers in the prose. Examples include:

- read features from a box plot;
- choose which distribution is harder to predict;
- identify an appropriate conditional percentage;
- distinguish independence from mutual exclusivity;
- interpret a sampling distribution or confidence interval;
- choose RSE, $R^2$, or a slope interval for a stated purpose;
- recode a reference category;
- recover group-specific slopes from an interaction;
- track one observation through cross-validation.

These remain useful candidates, but exercises are out of scope for the first
migration pass. They should be considered later as a separate pedagogical
revision rather than added incidentally while classifying prose.

## Preparation levels

- **Drop-in:** already a compact, locally complete passage. Mostly markup and
  title work.
- **Local rewrite:** the idea is clear, but its definition, example, formula,
  or interpretation currently overlaps neighboring prose.
- **Structural rewrite:** several paragraphs or a whole subsection must be
  reorganized so the callout does not duplicate the narrative or interrupt its
  logic.

The regression and inference chapters have the highest concentration of
structural-rewrite candidates because they repeatedly move between formal
statements, algebra, examples, and interpretive qualifications.

## Suggested adjudication order

1. Review existing callouts chapter by chapter and assign their target type.
2. Approve a small first migration consisting primarily of drop-in
   Definitions, Key ideas, Interpretations, and Technical details, with only
   unusually salient Warnings.
3. Decide which exact formulas belong in nested formula details versus
   numbered Technical details.
4. Return to local- and structural-rewrite candidates one chapter at a time,
   considering the surrounding prose before choosing exact boundaries.
5. Revisit inline Exercises in a separate pass.

This order tests the system in real chapters without committing to broad prose
restructuring at the outset.
