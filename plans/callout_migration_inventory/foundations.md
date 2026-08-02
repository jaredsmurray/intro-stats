# Foundations, single-variable, and two-variable chapters

Source-only candidate inventory. Line references are included for passages
without explicit section identifiers; they should be rechecked if the source
moves. This is intentionally selective.

## `index.qmd` — Preface

No strong callout candidate. The page is a short preface and reading list, with
no reusable definition, notation, technical aside, interpretation, warning, or
natural inline knowledge check. Adding a box here would give routine navigation
more visual weight than it warrants.

## `singlevar_01_visualizing-distributions.qmd` — Visualizing a Single Quantitative Variable

### Candidate 1

- **Anchor:** `## Histograms` (lines 69–71)
- **Type:** Definition
- **Content:** Histogram: divides a quantitative variable's range into bins and
  uses bar heights to show the count in each bin.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** This is the first formal reusable graphical object in the book
  and the paragraph is already locally complete.
- **Existing-callout overlap:** None.

### Candidate 2

- **Anchor:** `#sec-density-plots`, especially lines 118–136
- **Type:** Definition
- **Content:** Density plot, centered on the four properties students need to
  read one: nonnegative, height tracks nearby observations, total area is one,
  and interval area approximates a proportion.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** The definition and four-property list are a durable reference,
  but the current definition, explanation, and list would need a tighter
  boundary to avoid boxing too much surrounding narrative.
- **Existing-callout overlap:** None.

### Candidate 3

- **Anchor:** `### Comparing density plots and histograms`, lines 186–231
- **Type:** Warning/Common mistake
- **Content:** Histogram bin counts and density bandwidths are choices; vary
  them and do not treat small gaps or wiggles as stable features without
  checking sensitivity.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** The lesson is easy to lose across two figures, yet it guards
  against a common over-reading error and generalizes beyond the example.
- **Existing-callout overlap:** None.

### Candidate 4

- **Anchor:** `## Percentiles, quantiles, and the cumulative distribution function`,
  lines 277–285
- **Type:** Definition
- **Content:** Percentile, quantile, median, and quartiles, including the mapping
  between percentage and proportion forms.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** These tightly related terms are reused throughout the book and
  benefit from one retrievable reference rather than several disconnected
  boxes.
- **Existing-callout overlap:** None.

### Candidate 5

- **Anchor:** `## Box and violin plots`, lines 375–393
- **Type:** Warning/Common mistake
- **Content:** The 1.5-IQR rule flags potential outliers; it does not establish
  that an observation is erroneous or should be removed.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** This is a consequential and common misinterpretation. The
  current two-sentence paragraph is already concise.
- **Existing-callout overlap:** None.

### Candidate 6

- **Anchor:** Immediately after `#fig-boxplot-price`, lines 389–390
- **Type:** Exercise
- **Content:** Ask students to identify Q1, median, Q3, IQR, whiskers, and
  flagged points on the displayed box plot; solution maps each feature to the
  plot.
- **Confidence:** Medium
- **Preparation:** Local rewrite
- **Rationale:** This is a short visual decoding check with an unambiguous,
  compact solution, placed immediately after the relevant figure.
- **Existing-callout overlap:** None.

No strong notation or technical-detail candidate: the chapter's limited
notation is better kept with the percentile definitions, and the omitted
density-construction mathematics is not present in the source.

## `singlevar_02_describing-distributions.qmd` — Describing Distributions of Quantitative Variables

### Candidate 1

- **Anchor:** Chapter opening, lines 42–44
- **Type:** Key idea
- **Content:** Describe a quantitative distribution by location, spread,
  skewness, modality, and noteworthy extreme values.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** This is the chapter's organizing checklist and a useful
  retrieval aid for every later distribution description.
- **Existing-callout overlap:** None.

### Candidate 2

- **Anchor:** `#sec-symmetric-skewed`
- **Type:** Definition
- **Content:** Symmetric, right-skewed, and left-skewed distributions, with the
  tail—not the location of most observations—determining the direction of
  skew.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** The terms are foundational and students commonly name skew
  from the high part of the distribution rather than the long tail.
- **Existing-callout overlap:** None.

### Candidate 3

- **Anchor:** `## Multimodal distributions`
- **Type:** Definition
- **Content:** Bimodal/multimodal distributions as distributions with two or
  more distinct peaks.
- **Confidence:** Medium
- **Preparation:** Drop-in
- **Rationale:** It is a reusable term, though the section is already short and
  the gain from boxing it may be modest.
- **Existing-callout overlap:** None.

### Candidate 4

- **Anchor:** `## Outliers and extreme values`
- **Type:** Warning/Common mistake
- **Content:** An unusual value may be a real observation, a data problem, or an
  important subgroup; investigate it rather than automatically deleting it.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** This is a high-value analytic boundary and reinforces the
  box-plot warning in the preceding chapter without equating “extreme” with
  “bad.”
- **Existing-callout overlap:** None.

No strong notation or technical-detail candidate. A short exercise could ask
students to classify a displayed shape, but the source does not yet contain a
particularly natural prompt/solution pair worth prioritizing.

## `singlevar_03_location-and-spread.qmd` — Measuring Location and Spread

### Candidate 1

- **Anchor:** `#sec-measures-center`, lines 32–38
- **Type:** Definition
- **Content:** Mean and median, with the mean's formula available as
  `.formula-detail`.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** Both are core numbered definitions and should be retrievable
  together; hiding the exact mean formula in HTML keeps the conceptual
  comparison prominent.
- **Existing-callout overlap:** None.

### Candidate 2

- **Anchor:** `#sec-measures-center`, beginning line 40
- **Type:** Warning/Common mistake
- **Content:** A single measure of center can conceal bimodality or other
  important structure; inspect the distribution rather than reporting the
  center alone.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** This is the main limitation students should carry forward when
  using summary statistics.
- **Existing-callout overlap:** None.

### Candidate 3

- **Anchor:** `#sec-measures-spread`, lines 98–101
- **Type:** Interpretation
- **Content:** Spread as unpredictability: with the same information, the
  distribution with greater spread produces less precise guesses and larger
  typical prediction errors.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** This substantive interpretation unifies the chapter's several
  measures and is reused later for binary variables and modeling.
- **Existing-callout overlap:** None.

### Candidate 4

- **Anchor:** `#sec-measures-spread`, lines 110–114
- **Type:** Definition
- **Content:** Standard deviation, variance, and IQR; keep their conceptual
  meanings visible and place the exact standard-deviation formula in
  `.formula-detail`.
- **Confidence:** High
- **Preparation:** Structural rewrite
- **Rationale:** These are three reusable measures with different units and
  robustness properties. The current dense run of paragraphs needs deliberate
  boundaries rather than one oversized box.
- **Existing-callout overlap:** None.

### Candidate 5

- **Anchor:** Immediately after `#fig-zip-comparison`, lines 98–101
- **Type:** Exercise
- **Content:** Ask which ZIP's new sale price is harder to predict from ZIP code
  alone and why; solution identifies 78741 because its prices are more spread
  out.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** The source already poses the question and supplies a concise
  answer; it is almost exactly the intended inline-exercise pattern.
- **Existing-callout overlap:** None.

No separate notation callout is needed: notation belongs inside the relevant
definitions. No additional technical-detail candidate is strong beyond the
standard-deviation formula.

## `singlevar_04_transformations.qmd` — Transforming Quantitative Variables

### Candidate 1

- **Anchor:** Chapter opening and `#sec-linear-transformations`, lines 31–35
- **Type:** Definition
- **Content:** Transformation and linear transformation, including
  \(y=ax+b\).
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** These are durable terms and the linear form supports later
  work with standardization and regression.
- **Existing-callout overlap:** None.

### Candidate 2

- **Anchor:** Existing `Linear transformations and summary statistics` callout,
  lines 82–98
- **Type:** Key idea
- **Content:** How \(y=ax+b\) changes mean, median, standard deviation, and
  variance.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** This is already a coherent native note. Retyping it as a
  standard key-idea callout would align its semantics with the new system while
  keeping it unnumbered.
- **Existing-callout overlap:** Complete overlap with the existing
  `.callout-note`; this is a reclassification, not a second box.

### Candidate 3

- **Anchor:** `#sec-zscores`, lines 102–104
- **Type:** Definition
- **Content:** z-score and standardization; exact formula may remain visible or
  be placed in `.formula-detail` depending on the later formula policy.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** This is a highly reusable definition and compact enough to
  stand alone.
- **Existing-callout overlap:** None.

### Candidate 4

- **Anchor:** `#sec-returns`, lines 172–182
- **Type:** Definition
- **Content:** Relative change/arithmetic return, its sign interpretation, and
  the distinction from a linear transformation.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** The formula and interpretation are repeatedly reused in this
  and later chapters; consolidating them will make the convention easy to
  retrieve.
- **Existing-callout overlap:** None.

### Candidate 5

- **Anchor:** `#sec-logarithms`, lines 221–223
- **Type:** Warning/Common mistake
- **Content:** Logs require positive inputs; log base changes numerical units
  but not the fact that equal ratios become equal distances.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** Domain restrictions are easy to violate, while base confusion
  is common when the chapter moves from base-10 displays to natural-log
  returns.
- **Existing-callout overlap:** None.

### Candidate 6

- **Anchor:** `#sec-log-returns`, lines 277–321
- **Type:** Technical detail
- **Content:** Arithmetic/log-return conversion, multi-period compounding versus
  addition, and the small-return approximation; exact derivations and formulas
  in `.formula-detail`.
- **Confidence:** High
- **Preparation:** Structural rewrite
- **Rationale:** The material is correct and useful but long and algebraically
  interruptive relative to the chapter's conceptual flow. It is the strongest
  optional-disclosure candidate in this group of chapters.
- **Existing-callout overlap:** None.

### Candidate 7

- **Anchor:** Following the salary-raise example, lines 211–217
- **Type:** Exercise
- **Content:** Ask for the value after two equal percentage increases and
  whether two equal percentage decreases/increases cancel; concise solution
  applies multiplication to the changing base.
- **Confidence:** Medium
- **Preparation:** Local rewrite
- **Rationale:** A one-step compounding check prepares students for log returns
  without interrupting the narrative with a long exercise.
- **Existing-callout overlap:** None.

No strong standalone interpretation callout: the z-score comparison and
return examples are already closely tied to their figures and definitions.

## `singlevar_05_categorical.qmd` — Categorical Variables

### Candidate 1

- **Anchor:** `## Kinds of categorical variables`, lines 34–40
- **Type:** Definition
- **Content:** Categorical, nominal, ordinal, and binary variables.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** These form one reusable taxonomy. A single structured
  definition block is preferable to four consecutive boxes.
- **Existing-callout overlap:** None.

### Candidate 2

- **Anchor:** `## Frequency tables: counts and proportions`, lines 44–45
- **Type:** Definition
- **Content:** Frequency table, count, and proportion.
- **Confidence:** Medium
- **Preparation:** Drop-in
- **Rationale:** The terms recur, but the paragraph is simple enough that the
  visual emphasis should remain modest.
- **Existing-callout overlap:** None.

### Candidate 3

- **Anchor:** `#sec-dummy-variables`, lines 67–77
- **Type:** Definition
- **Content:** Dummy/indicator variable, including the 0/1 coding convention.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** This is a durable definition used throughout modeling, and the
  displayed mapping makes the block self-contained.
- **Existing-callout overlap:** None.

### Candidate 4

- **Anchor:** `## A proportion is the mean of a 0/1 variable`, lines 98–104
- **Type:** Key idea
- **Content:** The mean of a 0/1 indicator equals the proportion of
  observations coded 1; include the reading of \(\hat p\).
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** This is the chapter's central conceptual bridge and will be
  reused throughout inference and regression.
- **Existing-callout overlap:** None.

### Candidate 5

- **Anchor:** Existing `Where does \(\hat p(1-\hat p)\) come from?` callout,
  lines 126–145
- **Type:** Technical detail
- **Content:** Derivation of the variance of a binary variable.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** It is already optional algebra and directly matches the new
  technical-detail/formula-detail mechanism.
- **Existing-callout overlap:** Complete overlap with the existing collapsed
  `.callout-note`; migrate rather than duplicate it.

### Candidate 6

- **Anchor:** `### Good practice and pitfalls`, lines 248–262
- **Type:** Warning/Common mistake
- **Content:** The highest-value categorical-chart boundaries: preserve ordinal
  order, avoid truncated bar axes, and do not substitute decorative geometry
  for easy comparisons.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** The existing table is a useful checklist, but a selective
  warning should surface only the mistakes with real interpretive
  consequences, not box every style preference.
- **Existing-callout overlap:** None.

### Candidate 7

- **Anchor:** After the 0/1 mean identity, lines 98–104
- **Type:** Exercise
- **Content:** Give a short sequence of zeros and ones and ask for its mean and
  the corresponding event proportion; solution shows they are identical.
- **Confidence:** Medium
- **Preparation:** Local rewrite
- **Rationale:** A tiny calculation verifies the central identity before the
  variance discussion.
- **Existing-callout overlap:** None.

No strong standalone notation callout: \(\hat p\) should stay in the key-idea
block. The interpretation of binary variance is important but is better kept
as the narrative setup for the formula rather than boxed separately.

## `twovar_01_categorical-categorical.qmd` — Two Categorical Variables

### Candidate 1

- **Anchor:** `#sec-crosstabs`, beginning line 42
- **Type:** Definition
- **Content:** Cross-tabulation/contingency table: rows and columns represent
  categories and each cell counts one category combination.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** This is the chapter's basic data structure and is reused in
  probability and inference.
- **Existing-callout overlap:** None.

### Candidate 2

- **Anchor:** `#sec-joint-marginal-conditional`
- **Type:** Definition
- **Content:** Joint, marginal, and conditional proportions, organized around
  which total supplies the denominator.
- **Confidence:** High
- **Preparation:** Structural rewrite
- **Rationale:** The terms belong together and students' main difficulty is
  denominator selection. A compact reference after the three subsections would
  improve retrieval without boxing each worked calculation.
- **Existing-callout overlap:** None.

### Candidate 3

- **Anchor:** `#sec-independence-preview`
- **Type:** Definition
- **Content:** Independence of two categorical variables: the conditional
  distribution of one is the same across categories of the other (and matches
  the marginal distribution).
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** This is a precise, reusable meaning that will recur in
  probability and inference.
- **Existing-callout overlap:** None.

### Candidate 4

- **Anchor:** `#sec-joint-marginal-conditional`, after the conditional-proportion
  calculations
- **Type:** Warning/Common mistake
- **Content:** Conditional proportions use the total within the conditioning
  group; reversing “default among purpose X” and “purpose X among defaults”
  changes the denominator and answers a different question.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** Confusing the direction of conditioning is the central likely
  error in this chapter.
- **Existing-callout overlap:** None.

### Candidate 5

- **Anchor:** `#sec-independence-preview`, after the consumer-expectations table
- **Type:** Exercise
- **Content:** Ask whether outlook and income group appear independent by
  comparing the displayed conditional percentages; solution notes which row
  differences support the judgment.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** It is a short interpretation check using numbers already on
  the page, with no new calculation machinery.
- **Existing-callout overlap:** None.

No strong notation or technical-detail candidate. The formulas are short,
central arithmetic rather than interruptive derivations. No separate
interpretation callout is needed beyond the proposed exercise.

## `twovar_02_quantitative-quantitative.qmd` — Two Quantitative Variables

### Candidate 1

- **Anchor:** `#sec-scatterplots`
- **Type:** Definition
- **Content:** Scatterplot and the convention that each observation contributes
  one \((x,y)\) point.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** This is the foundational display for the chapter and a durable
  definition.
- **Existing-callout overlap:** None.

### Candidate 2

- **Anchor:** `#sec-cov-cor`, beginning around lines 122–132
- **Type:** Definition
- **Content:** Covariance and correlation; conceptual meaning visible, exact
  summation/scaling formulas in `.formula-detail`.
- **Confidence:** High
- **Preparation:** Structural rewrite
- **Rationale:** The paired concepts are central, but their derivation and
  geometric explanation are lengthy. Optional formulas would preserve the
  conceptual route through same-side/opposite-side deviations.
- **Existing-callout overlap:** None.

### Candidate 3

- **Anchor:** `#sec-cov-cor`, correlation properties around line 234
- **Type:** Interpretation
- **Content:** Correlation's sign gives direction, magnitude gives strength of a
  *linear* association, and unit changes do not alter it.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** This is the operational reading students need whenever they
  encounter \(r\).
- **Existing-callout overlap:** None.

### Candidate 4

- **Anchor:** `#sec-corr-limits` and its three subsections
- **Type:** Warning/Common mistake
- **Content:** Correlation measures only linear association, is sensitive to
  extreme observations, and is not a slope.
- **Confidence:** High
- **Preparation:** Structural rewrite
- **Rationale:** These are three tightly related boundaries and among the most
  consequential misconceptions in introductory statistics. A compact summary
  can point back to the full examples rather than replace them.
- **Existing-callout overlap:** None.

### Candidate 5

- **Anchor:** `#sec-best-fit-line`, lines 392–404
- **Type:** Definition
- **Content:** Least-squares line, including its criterion and the fact that it
  passes through \((\bar x,\bar y)\); place slope and intercept formulas in
  `.formula-detail`.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** This is a reusable definition and a strong use of optional
  exact formulas before the later regression treatment.
- **Existing-callout overlap:** None.

### Candidate 6

- **Anchor:** Following `#fig-austin-price-sqft-lm`, lines 449–450
- **Type:** Interpretation
- **Content:** Read a fitted value as an estimate of average \(y\) among
  observations near that \(x\), not as a guaranteed outcome for one
  observation.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** This is an important bridge from a drawn line to a substantive
  prediction and prevents deterministic readings.
- **Existing-callout overlap:** None.

### Candidate 7

- **Anchor:** `#sec-nonlinear`, lines 513–551
- **Type:** Warning/Common mistake
- **Content:** A smoother is a visual aid; especially near sparse boundaries or
  in small samples, do not treat every wiggle as evidence of real
  nonlinearity.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** The warning is concise, general, and directly addresses the
  main misuse of the tool.
- **Existing-callout overlap:** None.

### Candidate 8

- **Anchor:** After the Ford/Tesla correlation comparison and before
  `#sec-best-fit-line`
- **Type:** Exercise
- **Content:** Ask how two stocks can have similar correlations with the market
  but very different fitted slopes; solution invokes
  \(b=r(s_y/s_x)\) and their different volatilities.
- **Confidence:** Medium
- **Preparation:** Local rewrite
- **Rationale:** This checks the distinction between strength and scale at the
  exact transition where the chapter motivates slope.
- **Existing-callout overlap:** None.

No strong standalone notation callout: \(r\), \(s_x\), \(s_y\), \(a\), and
\(b\) are best introduced within the correlation and fitted-line definitions.

## `twovar_03_categorical-quantitative.qmd` — A Quantitative Variable Across Groups

### Candidate 1

- **Anchor:** Chapter opening, lines 46–50
- **Type:** Key idea
- **Content:** For a quantitative variable paired with a categorical variable,
  compute familiar summaries within groups and compare the group
  distributions.
- **Confidence:** High
- **Preparation:** Drop-in
- **Rationale:** This is the chapter's single organizing move and a useful
  bridge from the single-variable material.
- **Existing-callout overlap:** None.

### Candidate 2

- **Anchor:** `#sec-box-violin-by-group`, lines 99–125
- **Type:** Interpretation
- **Content:** Box plots emphasize compact comparisons of center/spread, while
  violin plots retain more distributional shape at the cost of visual
  complexity.
- **Confidence:** High
- **Preparation:** Local rewrite
- **Rationale:** This is a recurring visualization tradeoff worth surfacing
  after students have seen both displays.
- **Existing-callout overlap:** None.

### Candidate 3

- **Anchor:** `#sec-small-multiples`, especially lines 150–188
- **Type:** Key idea
- **Content:** Small multiples preserve each group's distributional shape;
  order panels by a meaningful summary to make comparison easier.
- **Confidence:** Medium
- **Preparation:** Local rewrite
- **Rationale:** The design principle generalizes across datasets, though much
  of its value is already visible in the figures.
- **Existing-callout overlap:** None.

### Candidate 4

- **Anchor:** After `#tbl-austin-price-by-zip`
- **Type:** Exercise
- **Content:** Ask which ZIP has the highest typical price and which has the
  greatest spread, requiring students to state whether they used mean/median
  and standard deviation/IQR; solution reads the relevant table columns.
- **Confidence:** Medium
- **Preparation:** Local rewrite
- **Rationale:** A short table-reading check reinforces that “typical” and
  “spread” require named summaries rather than a vague ranking.
- **Existing-callout overlap:** None.

No strong definition, notation, or technical-detail candidate in the live
chapter. The weighted-average formula and later examples are commented out and
therefore are not current candidates. No strong warning is present beyond
ordinary advice about meaningful ordering.

## `twovar_04_multivariate.qmd` — More Than Two Variables

No candidate from live prose: the file currently contains only front matter and
a commented planning note. The future topics suggest likely candidates
(conditioning/faceting as a key idea, Simpson's paradox as a warning, and a
multivariate-data definition), but recording them now would inventory a plan
rather than source content. There is likewise no current notation, technical
detail, interpretation, or exercise candidate.
