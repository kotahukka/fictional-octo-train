#!/usr/bin/env bash
set -euo pipefail

file=".VERSION"
current="$(cat "$file")"

# Expect vMAJOR.MINOR.PATCH
if [[ ! "$current" =~ ^v([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
  echo "ERROR: VERSION must be like v0.1.0 (got: $current)" >&2
  exit 1
fi

major="${BASH_REMATCH[1]}"
minor="${BASH_REMATCH[2]}"
patch="${BASH_REMATCH[3]}"

kind="${1:-patch}"

case "$kind" in
  major) major=$((major+1)); minor=0; patch=0 ;;
  minor) minor=$((minor+1)); patch=0 ;;
  patch) patch=$((patch+1)) ;;
  *) echo "Usage: $0 {major|minor|patch}" >&2; exit 2 ;;
esac

next="v${major}.${minor}.${patch}"
echo "$next" > "$file"
echo "Bumped VERSION: $current -> $next"
