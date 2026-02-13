#!/usr/bin/env bash
set -euo pipefail

# Replace literal tab characters with two spaces
# Only touch text files passed by pre-commit
for file in "$@"; do
  # Skip binary files
  if file "$file" | grep -q text; then
    perl -pi -e 's/\t/  /g' "$file"
  fi
done
