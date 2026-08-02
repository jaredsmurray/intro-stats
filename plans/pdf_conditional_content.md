# Add PDF fallbacks for animations and incompatible content

Status: **pending**

Create a standard conditional-content pattern for material that works in HTML
but cannot be rendered directly in PDF, including animations, interactive
widgets, and format-specific embeds.

## First known case

The full-book PDF currently fails when XeLaTeX reaches
`images/loess_construction.gif` in `regression_01_intro.qmd` because LaTeX
cannot determine a bounding box for the GIF.

## Plan

1. Inventory animated, interactive, and other format-specific content used by
   the book.
2. Define one maintainable authoring pattern using Quarto's format-conditional
   content:
   - retain the original animation or interactive in HTML;
   - provide a meaningful static image, sequence, table, or short explanation
     in PDF;
   - avoid duplicating surrounding prose.
3. Decide where fallback assets live and how they are generated. Generated
   images belong in `images/`; reusable generation scripts belong in
   `tools/figures/`.
4. Apply the pattern first to `images/loess_construction.gif`, then to the
   remaining inventory.
5. Add a deterministic check that flags incompatible assets included in the
   PDF path without a fallback.
6. Render and inspect both formats:
   - HTML retains the intended animation or interaction;
   - PDF contains the correct fallback with a useful caption;
   - cross-references and numbering remain stable;
   - a full PDF book build completes.

This is separate from the callout-infrastructure change. Do not add these
chapter-level conditionals while that branch remains infrastructure-only.
