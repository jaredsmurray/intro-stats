---
name: book-style
description: >
  Book-specific writing conventions for the "Introduction to Statistics and Data Science"
  textbook. Apply whenever drafting or editing natural-language chapter prose, including a new
  section, worked example, dataset write-up, or revision to a root chapter .qmd. Enforces six
  rules: introduce datasets fully once and remind briefly later; make structural moves without
  telegraphing them; use an accessible academic teaching voice; do not invent frameworks or broad
  claims without checking with Jared; weigh competing methods as tradeoffs rather than selling
  one; and follow the house terminology (machine-checked via style_terms.tsv). Triggers include
  "write a section," "draft a worked example," "revise this chapter," "add
  an example," "keep my voice," or any edit to chapter prose. Layers on Jared's voice pack. Does
  not apply to code chunks, data files, or YAML frontmatter.
---

# Book Style

Six book-specific rules for the statistics textbook, layered on top of Jared's general voice pack (loaded via the book's `AGENTS.md`). The first five are the writing moves most often gotten wrong when drafting or editing a chapter; the sixth is the house terminology, which is machine-checked. Apply all six to every piece of chapter prose; the voice pack covers everything else.

---

## 1. Introduce a dataset once, in full; remind only briefly after

The first time a dataset appears in the book, describe it at the level of detail the reader needs to follow the section: what it is, where it came from, its size, the unit of observation, and each variable the section actually uses. Define a variable the first time it does real work, not before.

After that first introduction, trust the reader's memory:

- **Later in the same stretch of work:** no re-introduction. Refer to the dataset and its variables by name.
- **After a gap** (a later chapter, or several sections spent on other data): a one-clause reminder of what the dataset is — nothing more.
- **New variables** from a familiar dataset: introduce and define each as it first comes up, even when the dataset itself is old news.

The aim is to inform without repeating. A reader who has just met the `lending` data does not need it re-explained two paragraphs later, and a reader meeting it again three chapters on needs a single clause of reminder, not the full provenance.

## 2. Do the move; do not telegraph it

Make structural moves without announcing them. If the instruction is "connect this to the example in Chapter 3," write the connection — do not open the paragraph with "Let's connect this to Chapter 3," and do not close it by naming the lesson. State the point and stop; trust the reader to feel the link.

**Telegraphing (bad):**

> The tallest bar is "same," but we leave it in the middle where it belongs. Because the categories are ordered, their sequence is part of the message — reading left to right traces sentiment from optimism to pessimism — and sorting by height would throw that away. The contrast with the purpose chart is the whole point: sort a nominal variable to expose a ranking, but preserve an ordinal variable's order to expose its shape.

**Doing (good):**

> The tallest bar is "same," but we leave it in the middle where it belongs. Because the categories are ordered, their sequence is part of the message — reading left to right traces sentiment from optimism to pessimism — and sorting by height would throw that away.

The good version stops once the point lands. The deleted sentence restated the takeaway the reader had already drawn. When you catch yourself writing "the whole point is," "this shows that," or "the contrast is," delete the sentence — the prose ahead of it already did the work.

Telegraphing also happens at the *front* of a move — announcing what's coming instead of just showing it:

**Telegraphing (bad):**

> Scatterplots have a failure mode worth knowing about before we go further. When the dataset is large, or one variable takes only a few distinct values, points stack on top of one another and the plot turns into unreadable ink --- a problem called **overplotting**. [...] the plot becomes a density map of its own ink.

**Doing (good):**

> When the sample size is large a scatterplot can turn into an unreadable blob. Even when the sample size is small, if one or both variables have many ties it can be difficult to read the scatterplot.

The bad version stages the problem before describing it ("a failure mode worth knowing about before we go further") and reaches for a flourish ("a density map of its own ink"). The good version starts with the problem itself, stated plainly.

The no-flourish rule applies to figure captions too:

**Flourish (bad):**

> Right: adding transparency turns density into darkness, and the plot becomes readable.

**Plain (good):**

> Right: adding transparency, so that darker regions hold more workers, makes the plot readable.

The bad caption trades information for a turn of phrase ("turns density into darkness"). The good caption says what the reader should take from the panel — darker means more workers — in the same number of words.

## 3. Accessible, academic teaching voice

Write like a patient instructor talking a student through the reasoning: warm, plain, and direct, but never breezy, salesy, or staged. Do not write like a consultant pitching a method or an LLM performing enthusiasm.

**Consultant / LLM-speak (bad):**

> Nothing in the last three sections was special to lending. To see that, let's run the same playbook — dummy variable, proportion, variance — on a new dataset.

**Accessible and academic (good):**

> Let's look at another example.

The bad version both telegraphs (it previews the "playbook") and performs (the staged reveal, the manufactured momentum). The good version simply hands off to the next example. Avoid manufactured momentum ("let's dive in," "here's the powerful part," "the key insight"), recaps that restate what was just done, and consulting-deck vocabulary ("playbook," "leverage," "unpack"). Prefer a plain sentence that moves the reader to the next idea.

## 4. Don't invent frameworks or broad claims; check them with Jared first

The book's conceptual structure — which distinctions get named, which taxonomies get taught, which claims get asserted as standard — comes from Jared, not from the draft. Do not import a framework from the wider literature, or invent a tidy breakdown, and present it as the book's teaching. If a section seems to want a piece of structure that the outline or prior chapters don't supply, ask before writing it in.

**Invented framework (bad — this breakdown wasn't in the prompt):**

> Three things are worth reading off any scatterplot, and this one has all three. **Direction**: the cloud tilts upward, so bigger homes tend to sell for more. **Strength**: the tilt is unmistakable but far from a perfect line --- pick any size, say 2,000 square feet, and prices at that size still range over several hundred thousand dollars. **Form**: the drift looks roughly straight, with no obvious bends. Hang onto that last observation, because "roughly straight" is exactly the condition under which the numerical summaries in the next section behave well.

**Describing what we see (good):**

> A scatterplot gives us a quick visual description of how the two variables tend to move *together*. We see here a positive relationship -- larger houses tend to sell for more -- that is close to *linear* (well-described by a straight line, rather than a U or some other shape) and fairly strong. We see some evidence that the variability in prices is larger for bigger houses -- the range of prices for houses around 1,000 sqft is narrower than the range of prices for houses around 3,000 sqft, for example.

The bad version teaches a bolded three-part taxonomy ("Direction / Strength / Form") the author never asked for, and the reader will expect the book to honor that structure forever after. The good version makes the same observations as observations, in plain prose, without minting vocabulary. Reading the data through concepts already established is fine; establishing new concepts is Jared's call.

## 5. Weigh competing methods; do not sell one

When the book puts two tools side by side --- histogram and density plot, box and violin plots, table and chart --- the section's job is to equip a choice, not to win one. The reader should leave knowing what each tool is good at, what that strength costs, and which situations call for which.

- Open the comparison with both sides' capabilities, mechanism attached, before any preference appears.
- Give parallel features parallel treatment. If both tools have a tuning choice (bins, bandwidths, smoothing), describe both the same way: what the choice is for, that defaults are sensible, that varying it and watching stability is good practice. Framing one tool's knob as a defect and the other's as a feature is advocacy, not analysis.
- State advantages as complements: one tool's strength is usually the other's cost, so write them as a pair ("the density's smoothing de-emphasizes small-sample gaps; the histogram's fidelity surfaces extreme values that may matter").
- Recommendations are conditional on use ("if precise values matter, use the table") and taste is marked as taste ("to my eye"). Never crown a winner ("the plot to reach for") and never personify virtues ("the honesty of the bars").
- An idiom may conclude an itemized argument ("so we get the best of both worlds:" — after the problems each tool solves have been listed); it may never replace the argument.

**Selling (bad):**

> A small bandwidth chases every little cluster, a large one irons the distribution flat, and the default sits in between. To my eye the default reads best here. The gain over the histogram is modest but real: the bandwidth is a single interpretable knob, and its default value is computed from the data rather than picked by hand.

**Weighing (good):**

> Small bandwidths act like many small bins, and large bandwidths act like a few [large] bins. The default bandwidth is chosen by some more involved statistical calculations. It's often quite good, particularly in large samples, but again it's a good idea to vary it a little and see how the picture changes.

The bad version scores the density plot against the histogram ("the gain over the histogram") and frames its tuning parameter as a feature — after the histogram's bin choice had been framed as a flaw. The good version gives the bandwidth exactly the treatment the bins got two paragraphs earlier: mechanism, sensible default, vary-and-check, no verdict. Note that even a well-formed judgment ("to my eye the default reads best here") was cut, because the judgment served the sales frame rather than the reader's choice.

## 6. House terminology

The book fixes canonical spellings for recurring terms. **Do not carry the list in your head.** The mechanically-decidable ones live in `style_terms.tsv` at the repo root and are enforced two ways: a `PostToolUse` hook runs `tools/check_terms.sh` after every edit, and `./tools/check_terms.sh --all` sweeps the whole book. If you drift on ZIP code, box plot, z-score, the `small-business` compound modifier, the em dash (`---`, never `--`), S&P 500, LendingClub, or CME FedWatch, the hook tells you in the same turn. Add a new canonical term by adding a row there, not by memorizing it — but only if a regex can decide it. The checker deliberately ignores code, `` `inline code` ``, `$math$`, HTML comments, and chunk-option lines other than `fig-cap`/`tbl-cap`, so those contexts are safe.

Three conventions a regex *can't* decide, so hold them yourself:

- **Samples in Latin, populations in Greek.** Latin letters for quantities
  computed from data — $\bar{x}$, $s$, $s^2$, $s_e$, $r$; operator and Greek
  notation — $\text{Var}(\cdot)$, $\text{SD}(\cdot)$, $\sigma^2$, $\epsilon$ —
  reserved for random variables and population/model parameters. Never write
  $\text{Var}(Y)$ for the variance of a data column. Corollary: students never
  fret about degrees of freedom. Divisor bookkeeping ($n$ vs $n-1$ vs
  $n-p-1$) gets at most one brief honesty pass where a quantity is defined
  (the standing examples live in singlevar_03 and regression_02); everywhere
  else, software counts the degrees of freedom and the difference never
  matters in any case we care about.

- **Dollar signs.** Escape as `\$` in body prose. But inside a YAML caption string (`fig-cap:`, `tbl-cap:`), write a raw `$` — a backslash there breaks the parse. So the same amount is `\$300{,}000` in a sentence and `$300,000` in a caption.
- **Probabilities on the [0,1] scale.** When the word "probability" carries the number, express it on [0,1] (`a probability of 0.05`), not as a percentage — in figure labels and axes too. Percentages are fine when the sentence is about a rate or share rather than a probability.

---

## The rest of the voice

These five rules are book-specific corrections. Jared's full writing voice — claims first, long-short sentence rhythm, a plain-English restatement after every formula, the banned-word list — is loaded from the voice pack via the book's `AGENTS.md`. Before drafting or revising chapter prose, read the rules and examples; before finalizing, run the checklist.

- Rules: `/Users/jm75583/Dropbox/voice-pack/voice/JARED_VOICE.md`
- Checklist: `/Users/jm75583/Dropbox/voice-pack/voice/JARED_CHECKLIST.md`
- Examples: `/Users/jm75583/Dropbox/voice-pack/voice/JARED_EXAMPLES.md`
- Worked sample: `/Users/jm75583/Dropbox/voice-pack/voice/test/rewrite_sample.md`
- To rewrite or audit a whole draft against the voice, use the `voice-draft` skill.
