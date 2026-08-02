# Callout regression fixture

This is a non-publishing, two-chapter Quarto book used only by
`tools/check_callouts.sh`. It exercises:

- all custom numbered block types and independent chapter counters;
- native Key idea, Interpretation, and Warning/Common mistake callouts;
- static and collapsible HTML behavior;
- formula-detail and solution disclosures;
- default-PDF formula omission and per-block inclusion; and
- the full-formula PDF profile.

The check command copies this fixture and the live infrastructure into a
temporary directory before rendering. No fixture chapter is part of the book's
published chapter list, and its solutions are never placed in a published
resource directory.
