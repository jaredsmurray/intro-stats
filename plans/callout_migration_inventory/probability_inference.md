# Probability and inference callout candidate inventory

Source-only review. Line numbers identify the present source location; section
IDs are the stable anchors. This inventory is intentionally selective and does
not propose exact callout boundaries or wording.

## `prob_01_intro.qmd` — Introduction to probability

1. **Anchor:** `#sec-what-is-probability`, lines 71–75
   - **Type:** Definition
   - **Content:** Probability as a numerical statement about an uncertain
     event, followed by the long-run-frequency and subjective interpretations.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** This is foundational vocabulary reused throughout the unit. A
     compact definition could separate the reusable meaning from the two
     interpretive perspectives, which should remain in the surrounding prose.
   - **Existing-callout overlap:** None.

2. **Anchor:** `#sec-what-is-probability`, lines 192–194
   - **Type:** Key idea
   - **Content:** Long-run-frequency and subjective probability are not
     separated by a bright line; each often depends partly on the other.
   - **Confidence:** Medium
   - **Preparation:** Drop-in
   - **Why:** This short qualification prevents students from treating the two
     interpretations as mutually exclusive camps and is easily lost after the
     extended FedWatch example.
   - **Existing-callout overlap:** None.

3. **Anchor:** `#sec-what-is-probability` → “Probability distributions,” line
   198
   - **Type:** Definition
   - **Content:** A probability distribution assigns probabilities to all
     possible outcomes of an uncertain process.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** This is a precise, reusable term and the bridge from observed-data
     distributions to probability distributions.
   - **Existing-callout overlap:** None; a fuller definition appears in
     `prob_02_probability-basics.qmd` at `#sec-prob-distributions`. Consider
     whether the introduction needs a numbered definition or only a key-idea
     preview to avoid duplicating the later canonical definition.

4. **Anchor:** `#sec-what-is-probability` → “What is a probability model?”,
   lines 202 and 219
   - **Type:** Definition
   - **Content:** A probability model is a probability distribution constructed
     to approximate a real process; parameters are features of that
     distribution, commonly estimated from data.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** “Probability model” and “parameter” are central terms introduced
     informally in the loan example and used throughout later chapters.
   - **Existing-callout overlap:** None.

5. **Anchor:** `#sec-what-is-probability` → “What is a probability model?”,
   line 219
   - **Type:** Warning/Common mistake
   - **Content:** A useful probability model need not be literally true; its
     adequacy depends on whether it captures the features relevant to the
     question.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** This is a durable modeling boundary that students may otherwise
     replace with “the fitted distribution is the truth.”
   - **Existing-callout overlap:** None.

6. **Anchor:** “What is sampling, and what is a sample?”, lines 223–236
   - **Type:** Key idea
   - **Content:** Sampling can mean selecting units from a population or
     observing repeated realizations from a probability distribution; both
     frames support the same inferential machinery.
   - **Confidence:** High
   - **Preparation:** Structural rewrite
   - **Why:** This is the chapter’s main conceptual bridge, presently spread
     across several paragraphs and a numbered summary. A short key-idea callout
     could provide a retrieval point after the explanation.
   - **Existing-callout overlap:** None.

7. **Anchor:** “What is sampling, and what is a sample?”, lines 229 and 234–236
   - **Type:** Warning/Common mistake
   - **Content:** Inference requires a sample representative of the target
     population or process; random sampling helps with sampling variation but
     historical data can still fail to represent future conditions.
   - **Confidence:** High
   - **Preparation:** Structural rewrite
   - **Why:** The distinction between sampling variability and
     representativeness is essential and anticipates `inference_03_limits.qmd`.
     The present footnote and nested list would need consolidation.
   - **Existing-callout overlap:** None.

8. **Anchor:** Loan choice prompt, lines 48–67
   - **Type:** Exercise
   - **Content:** Choose between the two otherwise identical loans, state the
     default probability used, and identify the assumptions needed to move from
     historical rates to a future-loan probability.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** The source already asks a short knowledge-check question and then
     immediately supplies the reasoning; it is a natural exercise with a
     concise collapsible solution.
   - **Existing-callout overlap:** None.

**No strong candidate:** Notation or technical-detail callouts. The chapter’s
notation is deliberately light, and the FedWatch mechanics are part of the
example rather than removable technical detail.

## `prob_02_probability-basics.qmd` — Probability basics

1. **Anchor:** `#sec-random-variables`, lines 46–50
   - **Type:** Definition
   - **Content:** Random variable, including the convention of capital-letter
     notation and its possible outcomes.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Precise reusable vocabulary and notation.
   - **Existing-callout overlap:** Existing `.callout-note` titled “Definition:
     Random variable”; migrate to the standardized numbered Definition block.

2. **Anchor:** `#sec-random-variables`, line 56
   - **Type:** Definition
   - **Content:** An event is a collection of possible outcomes and is the
     object to which probability is assigned.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** This precise term is used immediately in the probability rules
     and later conditional-probability work but is currently buried in prose.
   - **Existing-callout overlap:** None.

3. **Anchor:** `#sec-prob-rules`, lines 62–68
   - **Type:** Key idea
   - **Content:** The three fundamental probability rules.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** These are a compact reference rather than a new term, and students
     need to retrieve them repeatedly.
   - **Existing-callout overlap:** Existing `.callout-note`; restyle as an
     unnumbered Key idea rather than a Definition.

4. **Anchor:** `#sec-prob-rules`, lines 72–84
   - **Type:** Technical detail
   - **Content:** Derivation and formulas for the complement and general
     addition rules from the three axioms.
   - **Confidence:** Medium
   - **Preparation:** Local rewrite
   - **Why:** The rules are important, but the derivational explanation can
     interrupt readers who already grasp the set logic. Keep the operational
     statements visible and place only the algebra/derivation in optional
     detail.
   - **Existing-callout overlap:** Adjacent to the existing three-rules note;
     avoid nesting unless the standardized implementation supports it cleanly.

5. **Anchor:** `#sec-discrete-continuous`, lines 90–94
   - **Type:** Definition
   - **Content:** Discrete versus continuous random variables.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** This classification controls whether distributions are described
     with masses or densities and recurs throughout the probability unit.
   - **Existing-callout overlap:** None.

6. **Anchor:** `#sec-discrete-continuous`, line 94
   - **Type:** Key idea
   - **Content:** “Continuous” is often a useful mathematical abstraction even
     when measurements are technically discrete.
   - **Confidence:** Medium
   - **Preparation:** Drop-in
   - **Why:** It resolves a predictable objection without crowding the core
     discrete/continuous definition.
   - **Existing-callout overlap:** None.

7. **Anchor:** `#sec-prob-distributions` → “Discrete distributions,” lines
   104–108
   - **Type:** Definition
   - **Content:** Probability mass function.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Canonical reusable definition.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to the
     standardized numbered Definition block.

8. **Anchor:** `#sec-prob-distributions` → “Continuous distributions,” lines
   188–192
   - **Type:** Definition
   - **Content:** Probability density function.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Canonical reusable definition.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to the
     standardized numbered Definition block.

9. **Anchor:** `#sec-prob-distributions` → “Continuous distributions,” lines
   225–229
   - **Type:** Warning/Common mistake
   - **Content:** Density height is not probability; probabilities are areas,
     and an exact value has probability zero for a continuous random variable.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** The source explicitly identifies two common stumbling blocks, and
     both are prerequisite to correct continuous-probability calculations.
   - **Existing-callout overlap:** None.

10. **Anchor:** `#sec-prob-distributions` → “Continuous distributions,” lines
    231 and 275
    - **Type:** Definition
    - **Content:** Cumulative distribution function, including its
      discrete/continuous generality.
    - **Confidence:** High
    - **Preparation:** Local rewrite
    - **Why:** The CDF receives a precise reusable meaning and is needed later
      for quantiles and normal probabilities.
    - **Existing-callout overlap:** None.

11. **Anchor:** `#sec-prob-rules`, after lines 72–84
    - **Type:** Exercise
    - **Content:** Given two event probabilities and their overlap, compute an
      “or” probability; include a mutually exclusive case as a contrast.
    - **Confidence:** Medium
    - **Preparation:** Local rewrite
    - **Why:** A short calculation would check whether students know when
      probabilities add directly and when overlap must be subtracted.
    - **Existing-callout overlap:** None; this would require authoring a new
      prompt and solution rather than repackaging an existing question.

**No strong candidate:** Interpretation callout. The examples interpret their
probabilities locally, but no one passage needs separate emphasis.

## `prob_03_distribution-parameters.qmd` — Distribution parameters

1. **Anchor:** `#sec-rv-mean`, lines 75–85
   - **Type:** Definition
   - **Content:** Mean/expected value of a random variable and notation
     \(E[X]=\mu\).
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Canonical definition and notation reused throughout the rest of
     the book.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to a
     numbered Definition block. The formula could use `.formula-detail` if the
     visible definition is kept conceptual.

2. **Anchor:** `#sec-rv-mean`, lines 89–91 and 135
   - **Type:** Interpretation
   - **Content:** Expected value is a long-run average and need not itself be a
     possible outcome.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** This resolves the most common conceptual objection to expected
     value and has two strong source examples (coin indicator and Fed target
     midpoint).
   - **Existing-callout overlap:** Overlaps conceptually with the expected-value
     definition but should remain a separate unnumbered interpretation.

3. **Anchor:** `#sec-rv-median`, lines 139 and 183
   - **Type:** Definition
   - **Content:** The median as the smallest value where cumulative probability
     reaches 0.50, plus its robustness under skew.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** Precise reusable definition; the current single-sentence
     definition is easy to miss.
   - **Existing-callout overlap:** None.

4. **Anchor:** `#sec-rv-variance`, lines 189–199
   - **Type:** Definition
   - **Content:** Variance and standard deviation of a random variable, with
     \(\sigma^2\), \(\sigma\), and units.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Canonical definition and notation.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to a
     numbered Definition block. The summation and square-root formula are good
     `.formula-detail` candidates within it.

5. **Anchor:** `#sec-risk`, lines 254–277
   - **Type:** Key idea
   - **Content:** Equal expected values can conceal very different risks; risk
     is neither inherently good nor bad and choices balance expected outcomes
     against unpredictability.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** This is the section’s durable decision-making takeaway and is
     more important than either numerical loan example alone.
   - **Existing-callout overlap:** None.

6. **Anchor:** `#sec-rv-quantiles`, lines 281 and 309
   - **Type:** Definition
   - **Content:** Quantile and interquartile range for a probability
     distribution.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** Precise reusable concepts currently embedded in ordinary prose.
   - **Existing-callout overlap:** None.

7. **Anchor:** `#sec-shift-scale`, lines 315–323
   - **Type:** Key idea
   - **Content:** Mean and standard deviation under \(Y=aX+b\).
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** This is a compact transformation rule students will retrieve
     often, but it is not itself a definition.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to an
     unnumbered Key idea, with the equations optionally marked
     `.formula-detail`.

8. **Anchor:** `#sec-shift-scale`, lines 329–335
   - **Type:** Notation
   - **Content:** Standardization \(Z=(X-\mu)/\sigma\) and the meaning of a
     realized z-score.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** The symbol and convention recur in the normal and inference
     chapters.
   - **Existing-callout overlap:** None.

9. **Anchor:** “Continuous random variables,” lines 341–351
   - **Type:** Technical detail
   - **Content:** Integral formulas for continuous expected value and variance.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** The formulas are correct and useful as reference but explicitly
     not computationally central (“we will let software handle it”). Hiding them
     in HTML preserves the unchanged interpretations in the main flow.
   - **Existing-callout overlap:** Existing `.callout-note`; replace with a
     Technical detail or keep a short visible key idea with the integrals in
     `.formula-detail`.

10. **Anchor:** `#sec-rv-mean`, after the loan payoff calculation at lines
    93–110
    - **Type:** Exercise
    - **Content:** Recompute expected profit after changing the interest rate
      or default probability, then decide whether the loan is attractive on
      expected value alone.
    - **Confidence:** Medium
    - **Preparation:** Local rewrite
    - **Why:** The worked example already supplies all ingredients and supports
      a short calculation plus interpretation.
    - **Existing-callout overlap:** None; requires authoring a variant and
      concise solution.

**No strong candidate:** Warning/Common mistake beyond the expected-value
interpretation. The chapter’s main pitfalls are better handled by the proposed
Interpretation and Key idea callouts.

## `prob_04_normal.qmd` — The normal distribution

1. **Anchor:** `#sec-normal-pdf`, lines 79–89
   - **Type:** Notation
   - **Content:** \(X\sim N(\mu,\sigma^2)\), how to read \(\sim\), and the fact
     that the second parameter is variance although software commonly accepts
     standard deviation.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** This is exactly the kind of compact convention the standardized
     Notation block is designed to make retrievable.
   - **Existing-callout overlap:** Existing `.callout-note` explicitly titled
     “Notation”; migrate to the numbered Notation block.

2. **Anchor:** `#sec-normal-pdf`, line 91
   - **Type:** Key idea
   - **Content:** Linear transformations of a normal random variable remain
     normal, with transformed mean and variance.
   - **Confidence:** Medium
   - **Preparation:** Drop-in
   - **Why:** A concise closure property that is reused in sampling
     distributions.
   - **Existing-callout overlap:** None; overlaps with the general
     shifting/scaling key idea in `prob_03_distribution-parameters.qmd`.

3. **Anchor:** `#sec-normal-probabilities`, line 111
   - **Type:** Warning/Common mistake
   - **Content:** Modeling returns as normal is an approximation, not a literal
     claim; usefulness depends on the region and question, and assumptions
     should be checked.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** This is a model-interpretation boundary students need before
     applying normal probabilities mechanically.
   - **Existing-callout overlap:** None.

4. **Anchor:** `#sec-normal-probabilities`, lines 163–170
   - **Type:** Exercise
   - **Content:** Sketch and compute an interval probability in two ways:
     subtract CDF values or subtract the two outside tails.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** The source already presents two equivalent routes and a supporting
     figure, making this a natural knowledge check with a compact solution.
   - **Existing-callout overlap:** None.

5. **Anchor:** `#sec-empirical-rule`, lines 222–230
   - **Type:** Key idea
   - **Content:** The 68/95/99.7 rule.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** High-value compact reference, but not a definition.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to the
     standardized Key idea style.

6. **Anchor:** `#sec-standard-normal`, lines 291–295
   - **Type:** Warning/Common mistake
   - **Content:** A z-score has a probability interpretation only when the
     distributional shape is specified; the familiar normal tail probabilities
     are not universal.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Explicitly identified and already well bounded as a serious
     misconception.
   - **Existing-callout overlap:** Existing `.callout-important`; retain as the
     standardized Warning/Common mistake style.

7. **Anchor:** `#sec-qq-plots`, line 301
   - **Type:** Definition
   - **Content:** A QQ plot compares empirical and theoretical quantiles; a
     straight relationship supports the proposed distribution.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** Precise reusable diagnostic concept that students will need later.
   - **Existing-callout overlap:** None.

8. **Anchor:** `#sec-qq-plots`, lines 345 and 370
   - **Type:** Interpretation
   - **Content:** How sustained QQ-plot shapes indicate heavy tails, skew,
     light tails, or data artifacts, while small extreme-quantile deviations can
     occur even under normal sampling.
   - **Confidence:** High
   - **Preparation:** Structural rewrite
   - **Why:** The substantive reading rules are scattered across the definition
     paragraph and two result paragraphs. A compact interpretation reference
     could prevent visual diagnostics from becoming “points are/not on line.”
   - **Existing-callout overlap:** None.

**No strong candidate:** Technical-detail callout. The computations and QQ-plot
construction are central instruction rather than optional derivations.

## `prob_05_multivariate-distributions.qmd` — Multivariate distributions

1. **Anchor:** `#sec-joint-distributions`, lines 79 and 125–141
   - **Type:** Definition
   - **Content:** Joint probability distribution and marginal probability/
     distribution.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** These are core reusable terms. The joint definition is already
     compact; the marginal definition would need to be separated from the loan
     calculation.
   - **Existing-callout overlap:** None.

2. **Anchor:** `#sec-conditional-probability`, lines 145–155
   - **Type:** Definition
   - **Content:** Conditional probability and the “given that” bar notation.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Canonical definition and notation.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to a
     numbered Definition block. The formula can remain visible or use
     `.formula-detail` depending on the global formula policy.

3. **Anchor:** `#sec-conditional-probability`, lines 157–176
   - **Type:** Key idea
   - **Content:** Conditioning means restrict to outcomes consistent with the
     condition and renormalize; count-over-count and joint-over-marginal are the
     same calculation.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** This operational meaning is more memorable than the formula and
     connects directly to contingency-table work.
   - **Existing-callout overlap:** Adjacent to the existing conditional
     probability note; avoid duplicating its formula.

4. **Anchor:** `#sec-conditional-probability`, lines 178–185
   - **Type:** Warning/Common mistake
   - **Content:** Conditional probability is asymmetric:
     \(\Pr(A\mid B)\neq\Pr(B\mid A)\), with the tall/NBA base-rate example.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** This is a classic and consequential reversal error, clearly
     explained in a locally coherent passage.
   - **Existing-callout overlap:** None.

5. **Anchor:** `#sec-cme-joint`, line 336
   - **Type:** Key idea
   - **Content:** A probability tree and a joint table encode the same
     information: multiply along branches for joint probabilities and sum paths
     for marginals.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** This is the promised synthesis of the multi-chapter Fed example
     and a valuable retrieval rule.
   - **Existing-callout overlap:** None.

6. **Anchor:** `#sec-independence`, lines 342–357
   - **Type:** Definition
   - **Content:** Independence via product of marginals and equivalently via
     unchanged conditional distributions.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Canonical definition used throughout inference.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to a
     numbered Definition block. The equivalent formulas are plausible
     `.formula-detail` content if the intuitive statement stays visible.

7. **Anchor:** `#sec-rv-correlation`, lines 371–385
   - **Type:** Definition
   - **Content:** Covariance and correlation of random variables.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Canonical extension of the corresponding sample summaries.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to a
     numbered Definition block, likely with the expanded covariance summation
     in `.formula-detail`.

8. **Anchor:** `#sec-rv-correlation`, line 421
   - **Type:** Warning/Common mistake
   - **Content:** Independence implies zero correlation, but zero correlation
     does not imply independence.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** This one-way implication is frequently reversed and will matter
     when variance rules are invoked later.
   - **Existing-callout overlap:** None.

9. **Anchor:** `#sec-conditional-probability`, after lines 178–208
   - **Type:** Exercise
   - **Content:** Use the loan table to distinguish
     \(\Pr(D=1\mid P=\text{small business})\) from
     \(\Pr(P=\text{small business}\mid D=1)\), explaining the role of the base
     rates.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** The chapter already works both directions; withholding the second
     calculation would make a strong short misconception check.
   - **Existing-callout overlap:** None.

**No strong candidate:** Interpretation callout beyond the tree/table Key idea;
the loan and Fed numerical interpretations work best next to their respective
tables.

## `prob_07_combining-random-variables.qmd` — Combining random variables

1. **Anchor:** `#sec-lincom-rules`, lines 64–72
   - **Type:** Key idea
   - **Content:** Mean of a linear combination.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Compact, frequently reused rule rather than a definition.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to Key idea
     and consider `.formula-detail` for the general equation.

2. **Anchor:** `#sec-lincom-rules`, lines 78–92
   - **Type:** Definition
   - **Content:** Covariance and correlation.
   - **Confidence:** Medium
   - **Preparation:** Local rewrite
   - **Why:** The concepts are required locally, but their canonical definition
     already appears in `prob_05_multivariate-distributions.qmd`.
   - **Existing-callout overlap:** Existing `.callout-note`; likely replace
     with a short cross-reference/notation reminder rather than create a second
     numbered definition.

3. **Anchor:** `#sec-lincom-rules`, lines 98–110
   - **Type:** Key idea
   - **Content:** Variance of a linear combination, including the covariance
     term and the independent/uncorrelated special case.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** This is the algebraic engine for the portfolio chapter and needs
     a compact retrieval point.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to Key
     idea. The expanded general formula is a strong `.formula-detail` candidate
     while the independent special case may remain visible.

4. **Anchor:** `#sec-portfolio-risk`, lines 127–142
   - **Type:** Interpretation
   - **Content:** Portfolio expected return is a weighted average, while
     portfolio risk depends critically on correlation; the four correlation
     cases translate the variance formula into diversification behavior.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** This is the substantive meaning of an otherwise unintuitive
     formula and the central interpretation for the portfolio application.
   - **Existing-callout overlap:** None.

5. **Anchor:** `#sec-portfolio-data`, lines 320–323 and 431–433
   - **Type:** Key idea
   - **Content:** An asset that looks inferior in isolation can be the better
     portfolio addition because diversification depends on covariance with what
     is already held.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** This is the chapter’s strongest substantive takeaway and a useful
     correction to ranking assets by their standalone means and SDs.
   - **Existing-callout overlap:** None.

6. **Anchor:** `#sec-portfolio-data`, line 431
   - **Type:** Warning/Common mistake
   - **Content:** The highest estimated Sharpe ratio does not determine how much
     risk a person should take, and a ranking from a short historical window
     should not be treated as permanent.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Prevents a numerical summary from being overinterpreted as a
     universal portfolio prescription.
   - **Existing-callout overlap:** None.

7. **Anchor:** `#sec-sums-averages`, lines 439–453
   - **Type:** Key idea
   - **Content:** Means, variances, and SDs of sums and averages of iid random
     variables.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Central reference used immediately and in the inference chapters.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to Key
     idea, with the full formulas optionally in `.formula-detail`.

8. **Anchor:** `#sec-sums-averages`, lines 455 and 481
   - **Type:** Interpretation
   - **Content:** Aggregation makes totals more predictable relative to their
     size and reduces the SD of an average by \(1/\sqrt n\), without changing
     its mean.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** This is the intuitive result students need to carry into standard
     errors; it is more memorable than the formula alone.
   - **Existing-callout overlap:** Overlaps the sums/averages Key idea but
     supplies its substantive interpretation.

9. **Anchor:** `#sec-clt`, lines 517–531
   - **Type:** Key idea
   - **Content:** Central Limit Theorem for iid sums and averages.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** One of the book’s core results, but not a definition.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to Key
     idea. The two displayed approximations could use `.formula-detail` if a
     concise verbal statement remains visible.

10. **Anchor:** `#sec-clt`, lines 533 and 548
    - **Type:** Warning/Common mistake
    - **Content:** “Large enough” depends on the source distribution, and the
      CLT loss calculation relies on independence; common dependence can make
      the result wildly misleading.
    - **Confidence:** High
    - **Preparation:** Local rewrite
    - **Why:** These are the two conditions most likely to disappear when
      students memorize “sums become normal.”
    - **Existing-callout overlap:** None.

11. **Anchor:** `#sec-portfolio-risk`, after lines 137–140
    - **Type:** Exercise
    - **Content:** For the equal-weight, equal-risk portfolio, compute or rank
      portfolio SD under a new correlation and explain the diversification
      effect.
    - **Confidence:** High
    - **Preparation:** Local rewrite
    - **Why:** The source already provides four solved cases; one can become a
      short interpolation/check with a concise solution.
    - **Existing-callout overlap:** None.

**No strong candidate:** Notation callout. The symbols are introduced locally
and do not need a separate numbered convention beyond the existing definitions
and formulas.

## `inference_01_sampling-distributions.qmd` — Sampling distributions and confidence intervals

1. **Anchor:** `#sec-sap-dispute`, line 221
   - **Type:** Definition
   - **Content:** Estimation error \(\bar X-\mu\), including the fact that it
     cannot be calculated because \(\mu\) is unknown.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** A precise reusable concept that frames the entire inference unit.
   - **Existing-callout overlap:** None.

2. **Anchor:** `#sec-sap-dispute`, lines 223–249
   - **Type:** Technical detail
   - **Content:** Why a simple random sample from a large finite population can
     be modeled as iid draws from a discrete probability distribution, including
     the \(1/N\) derivation and negligible repeated-draw qualification.
   - **Confidence:** High
   - **Preparation:** Structural rewrite
   - **Why:** The source already labels this as an optional explanation (“if
     you're still wondering…”). It is conceptually sound but interrupts the
     route from the SAP dispute to sampling distributions.
   - **Existing-callout overlap:** None.

3. **Anchor:** `#sec-sampling-ci`, lines 270–274
   - **Type:** Definition
   - **Content:** Sampling distribution of a statistic.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Canonical definition.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to a
     numbered Definition block.

4. **Anchor:** `#sec-sampling-ci`, lines 278–292
   - **Type:** Key idea
   - **Content:** Across random samples, the sample mean is correct on average
     and its typical distance from the truth shrinks as sample size grows; the
     CLT supplies approximate normality.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** This is the main conceptual synthesis connecting earlier
     probability results to inference.
   - **Existing-callout overlap:** Adjacent to the standard-error definition;
     avoid repeating its formula.

5. **Anchor:** `#sec-sampling-ci`, lines 294–304
   - **Type:** Definition
   - **Content:** Standard error as the standard deviation of a sampling
     distribution, with the sample-mean formula and plug-in estimate.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Canonical definition used throughout inference.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to a
     numbered Definition block. The formula is a possible `.formula-detail`
     element if the conceptual definition remains visible.

6. **Anchor:** `#sec-sampling-ci`, lines 308–314
   - **Type:** Interpretation
   - **Content:** The SAP standard error of about 2.9 percentage points means a
     sample mean from 81 firms typically misses the population mean by about
     that amount; the observed 3.1-point gap is roughly one typical error.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Clean, substantive translation of the central numerical result.
   - **Existing-callout overlap:** None.

7. **Anchor:** `#sec-ci`, lines 397–405
   - **Type:** Definition
   - **Content:** 95% confidence interval and the approximate
     estimate-plus/minus-two-standard-errors recipe.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Canonical definition.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to a
     numbered Definition block.

8. **Anchor:** `#sec-ci`, lines 413 and 435
   - **Type:** Warning/Common mistake
   - **Content:** The 95% belongs to the repeated-sampling procedure, not the
     realized interval; the fixed \(\mu\) is either inside the observed interval
     or it is not.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** This is the canonical confidence-interval misinterpretation and
     presently sits well after the definition.
   - **Existing-callout overlap:** None.

9. **Anchor:** `#sec-bootstrap`, lines 447–451
   - **Type:** Definition
   - **Content:** Bootstrap algorithm and bootstrap standard error.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Canonical definition and procedure.
   - **Existing-callout overlap:** Existing `.callout-note`; migrate to a
     numbered Definition block.

10. **Anchor:** `#sec-bootstrap`, lines 455–469
    - **Type:** Technical detail
    - **Content:** Why bootstrap resamples have size \(n\), why sampling is with
      replacement, and why the bootstrap is not always preferable to analytic
      formulas.
    - **Confidence:** High
    - **Preparation:** Local rewrite
    - **Why:** Important qualifications, but interruptive once the basic
      algorithm is understood; the three present subheadings are already
      naturally modular.
    - **Existing-callout overlap:** None.

11. **Anchor:** `#sec-ci`, after lines 389–405
    - **Type:** Exercise
    - **Content:** Given an estimate and standard error, form an approximate 95%
      interval and state what the 95% does—and does not—mean.
    - **Confidence:** High
    - **Preparation:** Local rewrite
    - **Why:** Short arithmetic plus a misconception check fits the inline
      exercise format and reinforces the chapter’s central skill.
    - **Existing-callout overlap:** None.

**No strong candidate:** Notation callout. The symbols \(\bar X,\mu,\sigma,s\),
and \(n\) are introduced in context and already supported by prior chapters.

## `inference_02_hypothesis-tests.qmd` — Hypothesis tests and p-values

1. **Anchor:** Opening, lines 44–51
   - **Type:** Definition
   - **Content:** Hypothesis test, null hypothesis, and alternative hypothesis.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** Foundational reusable terms that currently appear in ordinary
     prose before the three-step framework.
   - **Existing-callout overlap:** None.

2. **Anchor:** Step 2, lines 67–82
   - **Type:** Definition
   - **Content:** The t-statistic as the observed difference from the null value
     measured in standard errors.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** Precise reusable statistic and interpretation.
   - **Existing-callout overlap:** None. The full substitution calculation is a
     candidate for `.formula-detail` inside the definition.

3. **Anchor:** Step 2, lines 84–112
   - **Type:** Definition
   - **Content:** The p-value as the probability, assuming the null hypothesis,
     of a test statistic at least as extreme as observed.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** Canonical definition at the center of the chapter.
   - **Existing-callout overlap:** None. The tail-area computation can be
     `.formula-detail`.

4. **Anchor:** Step 2, lines 76–84
   - **Type:** Warning/Common mistake
   - **Content:** The null distribution and p-value probability statement are
     conditional on the null hypothesis being true.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** The source emphasizes the condition twice because omitting it
     changes the meaning of both the test statistic and p-value.
   - **Existing-callout overlap:** Overlaps the proposed p-value definition but
     is important enough to keep visually explicit.

5. **Anchor:** Step 3, lines 114–120
   - **Type:** Key idea
   - **Content:** Tests reject or fail to reject a null; they do not establish
     that the null is true or false. Significance level \(\alpha\) sets the
     rejection threshold.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** A compact decision-language reference would support every later
     hypothesis test.
   - **Existing-callout overlap:** None.

6. **Anchor:** Step 3, lines 122–127
   - **Type:** Warning/Common mistake
   - **Content:** Failure to reject can result from imprecise data or from an
     estimate genuinely close to the null; neither proves the null.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** This directly blocks the common equation of “not significant”
     with “no effect.”
   - **Existing-callout overlap:** None.

7. **Anchor:** `#sec-ci-test`, lines 133–136
   - **Type:** Key idea
   - **Content:** A 95% confidence interval contains exactly the null values not
     rejected by the corresponding two-sided 5% test under the chapter’s normal
     approximation.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** Strong synthesis and a reusable diagnostic connection.
   - **Existing-callout overlap:** None.

8. **Anchor:** `#sec-ci-test`, lines 191–193
   - **Type:** Interpretation
   - **Content:** Identical p-values can accompany substantively different
     estimates and precision; confidence intervals distinguish those cases.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** This is the chapter’s strongest argument against treating the
     p-value as a complete report of evidence.
   - **Existing-callout overlap:** None.

9. **Anchor:** Step 2, after lines 67–112
   - **Type:** Exercise
   - **Content:** Given a sample estimate, null value, and SE, compute the
     t-statistic, locate the relevant two-sided tail area conceptually, and state
     the evidence without claiming the null is probably true.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** The worked SAP calculation can be converted into a compact
     knowledge check with an immediate solution.
   - **Existing-callout overlap:** None.

**No strong candidate:** Notation-only callout. \(H_0\) and \(H_A\) notation is
not yet used in the source, and introducing a standalone convention would be a
content decision beyond this inventory.

## `inference_03_limits.qmd` — Limits of statistical inference

1. **Anchor:** Opening, lines 5–9
   - **Type:** Warning/Common mistake
   - **Content:** The preceding confidence intervals and tests depend on
     treating the 81 firms as random or representative; the actual convenience
     sample does not justify that assumption.
   - **Confidence:** High
   - **Preparation:** Local rewrite
   - **Why:** This is the chapter’s central boundary and prevents readers from
     carrying mathematically correct sampling-error calculations beyond their
     design assumptions.
   - **Existing-callout overlap:** None.

2. **Anchor:** Lines 9–11
   - **Type:** Interpretation
   - **Content:** Even without representative sampling, the data can support a
     narrower conclusion: SAP’s advertised advantage is questionable, while a
     population-wide estimate is not warranted.
   - **Confidence:** Medium
   - **Preparation:** Local rewrite
   - **Why:** This is a nuanced translation from design limitations to the
     strongest defensible substantive claim. It should not be lost inside a
     generic “bad sample” warning.
   - **Existing-callout overlap:** None.

3. **Anchor:** Line 13
   - **Type:** Key idea
   - **Content:** Sampling variability is only one source of uncertainty;
     biased sampling, missing data, measurement error, and other defects are
     not captured by the simple confidence interval.
   - **Confidence:** High
   - **Preparation:** Drop-in
   - **Why:** This compact statement is the durable lesson of the chapter and
     the natural close to the introductory inference sequence.
   - **Existing-callout overlap:** None.

4. **Anchor:** After line 13
   - **Type:** Exercise
   - **Content:** Classify several threats in the SAP study as sampling
     variability versus representativeness/measurement problems, then state
     whether increasing \(n\) would fix each one.
   - **Confidence:** Medium
   - **Preparation:** Structural rewrite
   - **Why:** A short classification check would reinforce that larger samples
     reduce random error but do not automatically remove bias.
   - **Existing-callout overlap:** None; requires entirely new prompt and
     solution.

**No strong candidate:** Definition, notation, or technical-detail callouts.
The chapter is a short conceptual coda; adding formal boxes would work against
its compactness.
