# Shared preamble for the publishing scripts (ship.sh, publish.sh, clean.sh).
# Source from the repo root:  . tools/lib/preamble.sh
#
# Defines SITE_CLONE and SITE_URL from the untracked local config, and pins a
# UTF-8 locale before anything renders.

# Read one section of targets.conf: the lines between [name] and the next
# [section], minus blanks and comments. Consumers: ship.sh ([classify]),
# clean.sh and publish.sh ([render-dirs], [render-globs]).
targets_section() {
  awk -v s="[$1]" '$0 == s {f = 1; next} /^\[/ {f = 0} f && NF && $0 !~ /^#/' \
    targets.conf
}

# Per-machine config, deliberately untracked (documented in the course-kit
# BOOTSTRAP list): site.conf at the repo root holds exactly two lines,
#
#   SITE_CLONE=$HOME/builds/intro_stats_site
#   SITE_URL=https://jaredsmurray.github.io/intro-stats
#
# SITE_CLONE is where deploys compose (a gh-pages clone outside the repo);
# SITE_URL is what ship.sh byte-verifies against after a deploy. Environment
# values override for a one-off run.
if [ -f site.conf ]; then
  # shellcheck source=/dev/null
  . site.conf
fi
if [ -z "${SITE_CLONE:-}" ] || [ -z "${SITE_URL:-}" ]; then
  echo "ERROR: SITE_CLONE / SITE_URL are unset. Create site.conf at the repo" >&2
  echo "       root (untracked, per-machine) with those two lines; see" >&2
  echo "       tools/lib/preamble.sh for the expected values." >&2
  exit 1
fi
export SITE_CLONE SITE_URL

# R renders non-ASCII characters as literal "<U+XXXX>" text when it runs in the
# C locale, which is what an unset LANG gives you -- cron, launchd, or a shell
# started from Finder. The regression tables built by R/pkg/model_table.R emit a
# true minus sign (U+2212) and a superscript two (U+00B2), so a C-locale build
# publishes "R<U+00B2>" and "<U+2212>$435,551" into the tables. Nothing fails:
# the render is clean, quarto exits 0, and the wrong thing ships. Pin a UTF-8
# locale before anything renders.
if [ "$(locale charmap 2>/dev/null)" != "UTF-8" ]; then
  # Read the list once, then match against the string. Piping `locale -a`
  # straight into `grep -q` looks tidier but is wrong here: grep exits at the
  # first match, `locale -a` takes SIGPIPE, and `set -o pipefail` turns that
  # dead producer into a failed pipeline -- so the check reports "missing" for
  # a locale that exists. Codesets are spelled UTF-8 on macOS and utf8 on many
  # Linux builds, so accept either.
  available=$(locale -a 2>/dev/null || true)
  utf8_locale=$(printf '%s\n' "$available" | grep -ixm1 'en_US\.utf-\?8' || true)
  if [ -z "$utf8_locale" ]; then
    utf8_locale=$(printf '%s\n' "$available" | grep -ixm1 'C\.utf-\?8' || true)
  fi
  if [ -z "$utf8_locale" ]; then
    echo "ERROR: no UTF-8 locale available; rendered text would be mangled." >&2
    echo "Install/enable en_US.UTF-8, or run with LC_ALL set to a UTF-8 locale." >&2
    exit 1
  fi
  export LC_ALL="$utf8_locale" LANG="$utf8_locale"
fi
