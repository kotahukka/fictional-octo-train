#!/usr/bin/env python3
"""
Pre-commit helper: replace hard tabs with spaces in YAML files.

Behavior:
- For each file passed on argv, replace '\t' with '  ' (two spaces).
- If any file changes, rewrite it and exit 1 (so pre-commit stops and you re-stage).
- If nothing changes, exit 0.

This mirrors the behavior of auto-fixing hooks like end-of-file-fixer.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPLACEMENT = "  "  # two spaces


def process_file(path: Path) -> bool:
    try:
        original = path.read_text(encoding="utf-8")
    except Exception:
        # If we can't read it as text, skip quietly (pre-commit passes only text files typically)
        return False

    if "\t" not in original:
        return False

    updated = original.replace("\t", REPLACEMENT)
    if updated == original:
        return False

    path.write_text(updated, encoding="utf-8")
    print(f"Fixed tabs: {path}")
    return True


def main() -> int:
    changed_any = False
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.exists() and p.is_file():
            changed_any |= process_file(p)

    # If we modified files, fail so user re-adds changes (standard pre-commit pattern)
    return 1 if changed_any else 0


if __name__ == "__main__":
    raise SystemExit(main())
