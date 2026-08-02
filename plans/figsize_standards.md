# Figure size standards

Status: NOT STARTED. Replaces `todo/figure_text_size_bookwide.md`, whose
`base_size` sweep is **done** (all 21 chapters, 2026-07-29) and whose
`fig-width` recommendation was disproved — see "Carried-forward findings".

## 1. Choose defaults for figure layouts

Pick and document a default `fig-width` / `fig-height` / `base_size` for each
layout the book actually uses:

- a single ggplot
- patchwork 2x1 (two side by side)
- patchwork 1x2 (two stacked)
- patchwork 2x2

Defaults have to hold against the book's real constraint: the content column
caps at **702px** and never upscales, so anything wider than
`702/96 = 7.3in` is downscaled and its text shrinks with it. They also have to
survive the book's actual axis labels, which are frequently currency and
comma-formatted thousands — the binding constraint in practice (see item 3).

Open sub-questions:

- Where do the defaults live? A helper in `R/render/` that each chapter's setup
  chunk calls, `_quarto.yml` `fig-width`/`fig-height` defaults, or a documented
  convention with no enforcement.
- Does `base_size` stay flat at 13 across layouts, or scale down as panel count
  rises? The 13 parameterized `theme_minimal(base_size = 9 / 9.5 / 10)` calls
  still in the book are ad-hoc versions of exactly this, and should be replaced
  by whatever the standard says rather than individually tuned.
- Do slides get their own standard? `slides/*.qmd` is a separate revealjs
  project with a different column width; none of the 702px analysis transfers.

## 2. Check/enforce the standards for new content

A chunk whose `fig-width` and layout disagree with the standard should be
caught rather than noticed later during a visual review. Natural home is a
source-reading check next to `tools/check_terms.sh` and
`tools/check_number_consistency.R`, with the same `--hook` / `--all` shape and
the same ignore-file escape hatch for deliberate exceptions.

Also worth catching: an explicit `theme_minimal()` (or any `theme_*()`) appended
to a plot, which silently re-applies `base_size = 11` and overrides the
chapter's `theme_set`. That is the failure the just-completed sweep removed 82
instances of, and nothing currently stops it coming back.

## 3. Check for overlapping labels and unreadable text in generated figures

The hard one, and the reason item 1 can't be settled from source alone. A
figure can render successfully and still be unreadable — no warning, no error,
valid PNG.

Two known failure modes, both observed:

- **Axis label collision.** Narrowing a figure keeps text at full point size
  but gives it less horizontal room, so long labels overplot. At
  `fig-width: 7`, `singlevar_04`'s `fig-log-transform` renders its x-axis as
  `$0  $1,000,00 $2,000,00 ...` — overlapping and unreadable.
- **Text too small after downscaling.** Anything past 7.3in is scaled by
  `702/(96*w)`, shrinking all text below its nominal point size.

This needs to inspect rendered output, not source. Options to evaluate:
rendering each figure and testing label extents via `ggplot_build` /
`grid` grob widths before the PNG is written (catches collision exactly, needs
a render hook), or measuring text in the PNG itself. The `ggplot_build` route
is more promising and would also let the check *propose* a fix — a wider
`fig-width`, a shorter label format, or rotated labels.

Note that ~41 wide figures use `dollar_format()` or `comma_format()` on
large-magnitude axes. For those the real remedy is usually the label format
(`scale = 1e-6, suffix = "M"`), not the figure size — so the check should
suggest label changes, not just size changes.

## Carried-forward findings (verified, don't re-derive)

- **The 702px mechanism.** Quarto emits `<img class="img-fluid"
  width="{fig-width * 96}">`; Bootstrap's `img-fluid` is `max-width: 100%`, so
  it shrinks but never enlarges. The content column is
  `minmax(500px, calc(750px - 3em))` = 702px max. Verified in-browser.
- **"`base_size`, not `fig-width`, is the lever" is only true below 7.3in.**
  Above it, `fig-width` dominates and a `base_size` bump is scaled away.
  Measured 2026-07-29 on `fig-corr-panels` at base 9 vs 10.6, width 10 vs 7.
- **A blanket `fig-width` cap at 7 is wrong.** Of 66 chunks above width 7:
  1 safe (`fig-corr-panels`, the only one that blanks its axis text), 41 with
  wide currency/comma labels that collide when narrowed, 24 needing a look.
- **Four chapters have figures but no `theme_minimal`** — `prob_01_intro`,
  `prob_05_multivariate-distributions`, `twovar_04_multivariate`,
  `inference_03_limits` use ggplot's default grey theme. They were left out of
  the sweep on purpose: adding `theme_set(theme_minimal(13))` changes their
  appearance, not just their text size. `prob_05` has wide figures and is worth
  a decision.
- **Density y-axes render scientific notation** (`2e-06`, `4e-06`) in
  `singlevar_01` and `singlevar_04`, contradicting
  `todo/scientific_notation_render_check.md`'s claim that the book is clean.
  Belongs to that todo, noted here because it surfaces in every figure review.

Palette is deliberately out of scope — see `todo/color_palette_standard.md`.
