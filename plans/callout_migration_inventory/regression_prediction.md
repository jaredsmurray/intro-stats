# Regression and prediction candidates

This is a selective first pass. Line numbers are approximate source anchors;
section identifiers should be preferred when markup is eventually added.

## `regression_01_intro.qmd`

- `#sec-least-squares` (around line 88) — **Definition**: least-squares
  coefficients as the values minimizing average squared error. **High;
  local rewrite.** The definition is currently distributed across the
  objective function and following paragraphs; a compact box would give later
  chapters a referenceable statement.
- `#sec-residuals-fitted` (around lines 102–126) — **Notation**: fitted value
  $\hat y_i$, residual $e_i$, and the sign convention. **High; local rewrite.**
  The existing residual callout should become a numbered Definition, while a
  small adjacent Notation block could consolidate both symbols without
  repeating their interpretations.
- `#sec-residuals-fitted` (paragraph after `fig-example-residuals`) —
  **Warning/Common mistake**: a positive residual is not necessarily a good
  deal; it is conditional on the information in the model. **High; drop-in.**
  This is a compact, likely misconception already stated in prose.
- “Making predictions” (around line 206) — **Interpretation**: a fitted value
  is both a prediction for one case and an estimate of the average outcome
  among cases with the same predictors. **High; drop-in.** The existing
  two-bullet passage is already callout-shaped.
- “Interpreting the slope” (around line 243) — **Interpretation**: slope as a
  difference in predicted outcomes per unit difference in the predictor.
  **High; local rewrite.** Keep the numerical Austin reading in the box and
  leave the rise/run development in the narrative.
- “Interpreting the intercept” (around line 287) —
  **Warning/Common mistake**: an intercept has an algebraic interpretation but
  may be unreliable or substantively meaningless when zero is outside the
  observed predictor range. **High; drop-in.**
- “Multiple regression coefficients are adjusted comparisons” (around line
  367) — **Key idea**: each coefficient compares units that differ in one
  predictor and match on all others. **High; local rewrite.** This is the
  chapter's main transferable idea and should not be buried in the housing
  example.
- Immediately after that key idea — **Exercise**: interpret the negative
  bedroom coefficient for two equal-area houses, then explain why it need not
  conflict with the positive simple-regression coefficient. **High; local
  rewrite.** A short solution can reinforce adjusted versus unadjusted
  comparisons.
- No strong **Technical detail** candidate beyond putting the closed-form
  one-predictor coefficient formulas behind “Details and formulas”; those
  formulas are useful but interrupt the conceptual least-squares definition.

## `regression_02_prediction.qmd`

- `#sec-rse` (around lines 82–94) — **Definition**: residual standard error.
  **High; drop-in.** Convert the existing definition callout to a numbered
  Definition.
- Immediately after the RSE definition — **Interpretation**: RSE as typical
  prediction-error size, in outcome units, with direction varying across
  observations. **High; drop-in.**
- `#sec-r-squared` (around line 140) — **Definition**: $R^2$ as a relative
  reduction in residual variability compared with predicting by the outcome
  mean. **High; local rewrite.** The current development is longer than a
  definition; the box should hold the reusable statement while the figures
  motivate it.
- “What is $R^2$ measuring?” (around lines 181–200) — **Technical detail**:
  the variance decomposition and the equivalence
  $R^2=Var(\hat Y)/Var(Y)$. **High; drop-in.** This is precisely the sort of
  exact derivation that can be collapsed in HTML.
- Same section, eclipse example — **Warning/Common mistake**: predictive
  “variance explained” is not a causal or mechanistic explanation. **High;
  local rewrite.**
- Limitations list after the variance decomposition — **Warning/Common
  mistake**: $R^2$ is outlier-sensitive, misses nonlinear relationships, does
  not add across predictors, and does not measure decision accuracy or whether
  a slope differs from zero. **High; structural rewrite.** This is too large
  for one box as written; use one compact warning with four terse claims and
  keep examples outside.
- End of the limitations discussion — **Exercise**: choose RSE, $R^2$, or a
  slope interval for three questions: pricing accuracy, relative linear fit,
  and evidence of a relationship. **High; local rewrite.**

## `regression_03_model.qmd`

- “The LINE assumptions” (around line 223) — **Notation**: distinguish
  population coefficients $\beta$, true errors $\epsilon_i$, fitted
  coefficients $\hat\beta$, and residuals $e_i$. **High; local rewrite.**
  This would prevent the chapter's most consequential symbol confusion.
- Same section — **Definition**: the LINE regression model, preferably as one
  referenceable statement containing the mean model and iid normal errors.
  **High; local rewrite.**
- Conditional-model equation after the LINE display — **Interpretation**:
  among cases with the same $X=x$, outcomes follow a distribution centered on
  the population regression line with standard deviation $\sigma$. **High;
  drop-in.**
- `#sec` “Predictive Distributions and Prediction Intervals” (around line 269)
  — **Definition**: prediction interval as an interval targeting a new random
  observation, contrasted with a confidence interval targeting a fixed
  parameter. **High; local rewrite.**
- Same section — **Technical detail**: the plug-in predictive distribution and
  approximate $\hat y\pm2\widehat\sigma$ construction, including the caveat
  about parameter-estimation uncertainty. **High; drop-in.**
- “Model Diagnostics” opener (around line 311) — **Key idea**: assumptions
  concern unobservable true errors; diagnostics ask whether observable
  residuals behave as those errors should. **High; drop-in.**
- Equal-variance diagnostics (around lines 513–520) —
  **Warning/Common mistake**: assess spread around the smoother, not blindly
  around zero, and do not infer lower variance merely from sparse edge data.
  **High; drop-in.**
- “What if assumptions are violated?” (around line 522) — **Key idea**:
  prioritize linearity; other failures primarily threaten interval and test
  calibration when the mean structure remains sensible. **Medium; structural
  rewrite.** The current bullet list should be tightened before boxing.
- After the ERCOT coefficient table — **Exercise**: given a tiny slope p-value
  and a U-shaped residual plot, decide whether the linear model is adequate
  and what evidence controls that decision. **High; local rewrite.**

## `regression_04_categorical.qmd`

- Opening paragraph (around lines 107–111) — **Definition**: dummy variable as
  a 0/1 numerical representation of category membership. **High; local
  rewrite.** The earlier chapter introduced dummies, but this is their first
  regression-specific use.
- Existing callout around lines 163–169 — **Definition**: reference category.
  **High; drop-in.** Convert to the numbered Definition style.
- Directly after the reference-category definition —
  **Warning/Common mistake**: changing the reference category changes
  coefficient signs and meanings, but not fitted values, residuals, or model
  fit. **High; drop-in.**
- Two-category coefficient walkthrough (around lines 132–160) —
  **Technical detail**: plug in dummy values 0 and 1 to recover the two group
  means. **High; drop-in.** Keep the substantive result visible and collapse
  the algebra.
- `#sec-categorical-multiple-regression` (around lines 187–215) —
  **Interpretation**: categorical coefficients remain adjusted comparisons
  relative to the reference group, holding other predictors fixed. **High;
  local rewrite.**
- `#sec-zip-predictor` (around lines 255–310) — **Notation**: for $K$
  categories with an intercept, use $K-1$ dummy variables and identify the
  all-zero reference row. **High; local rewrite.**
- After the ZIP coding table — **Exercise**: change the reference from 78731
  to 78721 and identify the new intercept and two comparisons without
  refitting. **High; local rewrite.**
- Confidence-interval interpretation near line 180 —
  **Warning/Common mistake**: adjusted or unadjusted group differences are not
  automatically causal effects of group membership. **High; drop-in.**

## `regression_05_interactions.qmd`

- Existing callout around lines 195–199 — **Definition**: interaction as a
  term allowing one predictor's coefficient to depend on another predictor.
  **High; drop-in.** Convert to the numbered Definition style.
- Additive-versus-separate-lines setup before the definition — **Key idea**:
  no interaction imposes parallel fitted lines; an interaction allows slopes
  to differ. **High; local rewrite.**
- Algebra plugging in `male = 0` and `male = 1` (around lines 229–265) —
  **Technical detail**: derive group-specific intercepts and slopes from the
  common interaction model. **High; drop-in.**
- “Interpreting the coefficients” (around line 270) —
  **Interpretation**: each main effect is conditional on the interacting
  predictor equaling zero, while the interaction coefficient is a
  difference-in-slopes. **High; structural rewrite.** The four existing
  bullets could become a compact interpretation box after trimming repeated
  arithmetic.
- “Main effects and hierarchy” (around line 286) —
  **Warning/Common mistake**: do not interpret a main effect as an overall
  effect when an interaction is present; retain lower-order terms when using
  an interaction. **High; local rewrite.**
- Centering discussion (around lines 382–430) — **Technical detail**:
  centering changes coefficient reference points, not fitted values,
  residuals, predictions, or $R^2$. **High; local rewrite.**
- After the first interaction table — **Exercise**: use four reported
  coefficients to recover the two group-specific slopes and their difference.
  **High; local rewrite.**

## `regression_06_nonlinear.qmd`

- “Log transformations in regression” (around line 302) — **Key idea**:
  logging the outcome turns additive linear-predictor contributions on the log
  scale into multiplicative contributions on the original scale. **High;
  local rewrite.**
- Exponentiation development immediately after the fitted model —
  **Technical detail**: factor the exponentiated prediction into multiplicative
  contributions. **High; drop-in.**
- Diagnostics discussion (around lines 366–405) —
  **Interpretation**: constant variance after logging means approximately
  constant multiplicative/percentage error, not constant dollar error.
  **High; drop-in.**
- Coefficient interpretation (around lines 410–560) — **Technical detail**:
  exact ratios via $\exp(\beta\Delta x)$ versus the small-change percentage
  approximation. **High; structural rewrite.** Split the reusable rule from
  the Austin arithmetic.
- Same passage — **Warning/Common mistake**: do not read a log-scale
  coefficient as an exact percentage for large changes. **High; drop-in.**
- `#sec-polynomial-regression` (around line 699) — **Definition**: degree-$k$
  polynomial regression includes powers $X,\ldots,X^k$ and all lower powers.
  **High; local rewrite.**
- After the polynomial definition — **Interpretation**: focus on the fitted
  curve's overall shape rather than individual raw-power coefficients.
  **High; drop-in.**
- “Overfitting and extrapolation” (around line 834) —
  **Warning/Common mistake**: high-degree polynomials may behave reasonably
  inside the data and wildly just outside it; in-sample fit cannot select a
  reliable degree. **High; local rewrite.**
- Polynomial section — **Exercise**: compare degree-2 and degree-9 curves and
  identify which evidence speaks to fit, overfit, and extrapolation. **Medium;
  local rewrite.**
- Unnumbered log appendix (around line 966) — **Notation** or
  **Technical detail**: compact log/exponential identities and exact
  ratio/percentage conversion. **Medium; structural rewrite.** This may work
  better as a reference block than as a continuous appendix.
- Log appendix final paragraph — **Warning/Common mistake**: zero and negative
  values cannot be logged, and adding an arbitrary constant changes ratios and
  substantive meaning. **High; drop-in.**

## `prediction_01_error.qmd`

- `#sec-new-data-in-sample` (around line 487) — **Definition**: new-data
  prediction error versus in-sample residual error. **High; local rewrite.**
- ERCOT comparison (around lines 495–514) — **Warning/Common mistake**:
  compare the shapes of training/test error curves when years differ in
  baseline difficulty; their absolute levels need not be directly comparable.
  **High; drop-in.**
- `#sec-bias-variance` (around line 516) — **Definition**: underfitting,
  overfitting, bias, variance, and irreducible error. **High; structural
  rewrite.** This likely needs two coordinated blocks: a core Definition and a
  Key idea tied to the U-shaped error curve.
- Same section — **Technical detail**: expected squared prediction error as
  squared bias plus variance plus irreducible error, stated without proof.
  **High; drop-in.**
- `#sec-training-testing` (around line 541) — **Definition**: training and
  testing data. **High; drop-in.**
- Immediately after the train/test diagram — **Warning/Common mistake**:
  information from a test observation must not enter model fitting or model
  selection; once used for selection, it is no longer untouched test data.
  **High; local rewrite.**
- Test RMSE display (around lines 551–560) — **Notation**: test RMSE and its
  relationship to RSE. **Medium; drop-in.**
- Random-split discussion (around lines 564–605) — **Interpretation**:
  random splits estimate performance for new cases from a similar population,
  not future regimes or new locations. **High; drop-in.**
- Existing five-fold procedure callout (around lines 611–628) —
  **Definition**: five-fold cross-validation. **High; local rewrite.** Convert
  to a numbered Definition; keep the numbered procedure, but add the core
  one-sentence meaning.
- Immediately after that procedure — **Warning/Common mistake**: five folds
  do not create five independent datasets; together they create one complete
  set of held-out predictions. **High; drop-in.**
- Cross-validation section — **Exercise**: for one named observation, count
  how many folds use it for training and testing, then explain why candidate
  models must share fold assignments. **High; local rewrite.**

## `appendix_data.qmd`

No strong callout candidates. This appendix is reference documentation; boxes
would compete with its dataset-entry structure. Individual included dataset
files may eventually merit provenance warnings, but that requires a separate
data-documentation review.

## `data.qmd`

No strong callout candidates. This is a download index, not expository prose.
Keep the single introductory note about gzipped CSV support as ordinary prose.
