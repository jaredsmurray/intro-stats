# Book-wide color palette: pick a standard, don't roll our own

Status: NOT STARTED — decision needed before any code moves. Supersedes the
single-color-literal half of `todo/set2_palette_rollout.md` (see below).

Jared, 2026-07-29: the book should standardize on **one** palette book-wide,
drawn from an established, well-tested set rather than a hand-assembled one.

## Why the Set2 rollout was stopped

A pilot on `twovar_02` and `singlevar_01` (2026-07-29) converted the bare
`steelblue`/`darkorange` literals to Set2 teal `#66C2A5` / salmon `#FC8D62`
and was reverted. Two problems showed up immediately, and both are properties
of the approach, not of those two files:

1. **Three-color figures break.** `fig-austin-price-sqft-lm-smooth` draws teal
   points, a salmon fit line, and a `darkgreen` loess smoother. Teal points and
   a dark green curve are the same hue family, so the smoother stopped
   separating from the cloud — it had separated cleanly when the points were
   `steelblue`. `regression_03_model.qmd`'s diagnostics have the same shape.
   Substituting two literals at a time cannot see the third color already in
   the figure.
2. **It is still hand-rolled.** Picking Set2's first two entries for
   *ungrouped* single-color marks is a local convention, not a palette. It
   gives no answer for the third or fourth color in a figure, for sequential or
   diverging scales, or for the semantic colors already in use.

## What the standard has to cover

The book currently mixes at least five color systems. Any candidate needs a
ruling for each:

- **Single-color marks** (~185 literals: `fill = "steelblue"`,
  `color = "darkorange"` — plain histogram fills, boxplots, reference lines,
  annotations). The bulk of the work.
- **Qualitative groups** — already ColorBrewer Set2 via `scale_*_brewer` in
  `regression_04`/`05`/`06`. Converted; leave or migrate with the rest.
- **Ordered counts** — viridis, per `regression_01`'s bedrooms.
- **Diverging** — `regression_03:412,465` uses `gradient2` ("Red points ...
  blue for less").
- **Semantic app colors** — `inference_01`'s red X / red intervals / purple
  curve, deliberately excluded from the earlier sweep. Note the caption at
  `:429` builds the word "red" out of `sum(!app_hits[1:100])`.
- **Interactive hover states** — `singlevar_01:105,333,361`
  `opts_hover(css = "fill:darkorange;")`. Palette or UI affordance? Undecided.

Also needs a call on whether the standard extends to `slides/*.qmd` (a separate
revealjs project) and to `webapps/`, which the Set2 plan put out of scope.

## Candidates worth evaluating

Prefer something with a published rationale, colorblind-safe checks, and an
off-the-shelf ggplot2 scale — so the choice can be cited rather than defended:

- **Okabe-Ito** — designed for colorblind safety, 8 colors, in base R as
  `palette.colors(palette = "Okabe-Ito")`. Ships with a neutral grey.
- **ColorBrewer** qualitative/sequential/diverging families — already partly
  adopted, covers all three scale types from one source, `scale_*_brewer`.
- **viridis** family — already used for ordered counts; weak for qualitative.
- **Tableau 10 / `ggthemes`** — well-tested qualitative defaults.

Selection criteria: colorblind-safe; readable at the alpha levels the book
actually uses (many marks are `alpha = 0.3`); enough separation for the
three-color figures above; and a defined answer for sequential and diverging,
not just qualitative.

## Trap that survives from the Set2 plan

**Prose that names a color is coupled to figure code, and nothing in the render
catches a mismatch.** The pilot hit three in two files
(`singlevar_01:133` "the blue area", `twovar_02:455` "solid orange",
`twovar_02:522` "(orange) and a smooth curve (green)"), and five more are known
in `regression_03` (~334, 378, 494) and `prob_04_normal`. One is a decoy:
`twovar_02:515` describes `images/loess_construction.gif`, an external asset a
code sweep would not recolor, so its "orange" must stay. Grep color words in
any pass that changes a palette, and check whether each one points at generated
or external art.

The full inventory of color sites and the eight coupled prose references is in
`todo/set2_palette_rollout.md` — that file's *inventory* is still good; only its
recommendation (Set2 teal/salmon for single-color literals) is withdrawn.

## Sequencing

The `base_size` sweep this was originally meant to ride along with is **done**
(2026-07-29, all 21 chapters), so that merge opportunity has passed — a palette
change now pays for its own full-book render and visual review.

The remaining figure work is `todo/figsize_standards.md`, which will need a
render review of its own. If the palette decision lands before that executes,
merge the two passes; otherwise budget for two reviews.
