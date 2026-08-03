# Book CI render — costs and benefits

Status: proposed, not built (Jared's call on whether/when). Tracking Issue
links here; this file owns the design detail.

## What it is

A GitHub Actions workflow that proves the public book renders from nothing:
checkout → install Quarto + R + package dependencies → `tools/get_data.sh`
(anonymous; the fetch skips the one restricted dataset, which no chapter
reads) → full `quarto render` → run `tools/checks/` (terms, number
consistency, unicode escapes, review-history consistency). Trigger: weekly
schedule plus on push to main.

## Benefits

- **The drift detector this repo was designed around** (refactor plan risk
  9): the book's core promise is that a fresh clone renders — CI is the only
  thing that verifies the promise continuously rather than at release
  moments. Catches silently-broken data URLs, package-version drift, and
  Quarto upgrades that break the patched callout extension
  (`CALLOUT_PATCHES.md` — historically the most upgrade-fragile piece).
- Catches contributor-machine assumptions (fonts, locale, TeX, PATH) that
  local renders hide — the class of failure that otherwise appears the week
  a semester starts.
- Zero secrets needed: the whole render path is public as of v2026.09.

## Costs

- **Wall-clock and quota**: the full render is ~10 minutes locally; on a
  cold GitHub runner with R package installation it is realistically 25–45
  minutes unless the R library is cached. Public-repo Actions minutes are
  free, so the cost is latency and maintenance, not money.
- **Cache maintenance**: an renv/pak lockfile or setup-r-dependencies cache
  is effectively required to keep runs under ~15 minutes; that lockfile
  becomes one more thing that drifts (the book has no renv today — adding
  one is the real work in this task).
- **Flake surface**: CRAN outages, GitHub release-asset hiccups, and Quarto
  installer changes will produce red runs that mean nothing; expect an
  occasional morning of "CI is lying."
- **TeX**: only needed if the callout PDF regression check joins CI;
  recommend leaving it local-only at first (HTML render is the core gate).

## Recommendation

Worth building before the semester, in the minimal form: HTML render + checks,
weekly + on-push, R packages cached via `setup-r-dependencies` with a DESCRIPTION
file listing the book's packages (lighter than full renv). Defer TeX/PDF and any
deploy-from-CI ambitions — publish.sh remains the only deployer.
