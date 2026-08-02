# Introduction to Statistics and Data Science — Claude instructions

The shared project instructions are in `AGENTS.md` (the single source — edit
there, not here):

@AGENTS.md

## Claude-specific notes

- House terminology and displayed-number precision are both machine-checked:
  `PostToolUse` hooks run `tools/check_terms.sh` and
  `tools/check_number_consistency.R` after Claude's edits. Hand edits made
  directly in an editor never hit either hook — sweep with
  `./tools/check_terms.sh --all` (`--fix` to apply) and
  `./tools/check_number_consistency.R --all`.
