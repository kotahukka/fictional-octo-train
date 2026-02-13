"""
Version bump utility for fictional-octo-train.

Usage:
python scripts/bump_version.py patch
python scripts/bump_version.py minor
python scripts/bump_version.py major
"""

from **future** import annotations

import re
import sys
from pathlib import Path

VERSION_FILE = Path(".VERSION")
VERSION_PATTERN = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")

def parse_version(version: str) -> tuple[int, int, int]:
match = VERSION_PATTERN.match(version.strip())
if not match:
raise ValueError(f"Invalid version format: {version!r} (expected vMAJOR.MINOR.PATCH)")
return tuple(int(part) for part in match.groups())

def bump_version(major: int, minor: int, patch: int, kind: str) -> tuple[int, int, int]:
if kind == "major":
return major + 1, 0, 0
if kind == "minor":
return major, minor + 1, 0
if kind == "patch":
return major, minor, patch + 1
raise ValueError("Usage: bump_version.py {major|minor|patch}")

def main() -> int:
if len(sys.argv) != 2:
print("Usage: bump_version.py {major|minor|patch}", file=sys.stderr)
return 2

    kind = sys.argv[1]

    if not VERSION_FILE.exists():
        print(f"ERROR: {VERSION_FILE} not found.", file=sys.stderr)
        return 1

    current_raw = VERSION_FILE.read_text().strip()

    try:
        major, minor, patch = parse_version(current_raw)
        new_major, new_minor, new_patch = bump_version(major, minor, patch, kind)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    new_version = f"v{new_major}.{new_minor}.{new_patch}"
    VERSION_FILE.write_text(new_version + "\n")

    print(f"Bumped .VERSION: {current_raw} -> {new_version}")
    return 0

if **name** == "**main**":
raise SystemExit(main())
