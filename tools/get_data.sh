#!/usr/bin/env bash
#
# get_data.sh -- materialize the pinned course datasets into ./data.
#
# The pin is the one-line `data_pin` file at the repo root (a teaching-data
# release tag). Change the pin, re-run this, and every number in the book is
# rebuilt from that version.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ -f "$ROOT/data_pin" ] || { echo "error: no data_pin at repo root" >&2; exit 1; }
TAG="$(tr -d '[:space:]' < "$ROOT/data_pin")"
[ -n "$TAG" ] || { echo "error: data_pin is empty" >&2; exit 1; }

exec "$ROOT/tools/fetch_data.sh" "$TAG" "$ROOT/data"
