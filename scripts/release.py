#!/usr/bin/env python3
"""
Tag-driven release helper for fictional-octo-train.

Flow:
- require clean git working tree
- bump .VERSION using scripts/bump_version.py
- commit .VERSION
- create annotated tag matching .VERSION
- push commit and tag

Usage:
  python scripts/release.py patch
  python scripts/release.py minor
  python scripts/release.py major

Or:
  ./scripts/release.py patch
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

VERSION_FILE = Path(".VERSION")
VERSION_RE = re.compile(r"^v\d+\.\d+\.\d+$")


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=check)


def die(msg: str, code: int = 1) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return code


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], check=check)


def ensure_git_repo() -> int:
    cp = git("rev-parse", "--show-toplevel", check=False)
    if cp.returncode != 0:
        return die("Not inside a git repository.")
    return 0


def ensure_clean_tree() -> int:
    cp = git("status", "--porcelain")
    if cp.stdout.strip():
        print(cp.stdout, end="", file=sys.stderr)
        return die("Working tree is not clean. Commit or stash changes first.")
    return 0


def read_version() -> str:
    if not VERSION_FILE.exists():
        raise FileNotFoundError(f"{VERSION_FILE} not found.")
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def ensure_version_format(version: str) -> int:
    if not VERSION_RE.match(version):
        return die(f".VERSION must be vMAJOR.MINOR.PATCH (got: {version!r}).")
    return 0


def ensure_tag_missing(tag: str) -> int:
    cp = git("rev-parse", tag, check=False)
    if cp.returncode == 0:
        return die(f"Tag {tag} already exists.")
    return 0


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"major", "minor", "patch"}:
        print("Usage: release.py {major|minor|patch}", file=sys.stderr)
        return 2

    kind = sys.argv[1]

    rc = ensure_git_repo()
    if rc:
        return rc

    rc = ensure_clean_tree()
    if rc:
        return rc

    bump_py = Path("scripts/bump_version.py")
    if not bump_py.exists():
        return die("scripts/bump_version.py not found.")

    # Bump .VERSION
    cp = run([sys.executable, str(bump_py), kind], check=False)
    if cp.returncode != 0:
        print(cp.stdout, end="")
        print(cp.stderr, end="", file=sys.stderr)
        return die("Version bump failed.")

    version = read_version()
    rc = ensure_version_format(version)
    if rc:
        return rc

    rc = ensure_tag_missing(version)
    if rc:
        return rc

    # Commit .VERSION bump
    git("add", str(VERSION_FILE))
    cp = git("commit", "-m", f"chore(release): bump version to {version}", check=False)
    if cp.returncode != 0:
        # commit might fail if no changes, but bump_version should always change
        print(cp.stdout, end="")
        print(cp.stderr, end="", file=sys.stderr)
        return die("git commit failed.")

    # Tag and push
    git("tag", version)
    git("push")
    git("push", "origin", version)

    commit = git("rev-parse", "--short", "HEAD").stdout.strip()

    print("\nRelease prepared:")
    print(f"  Version: {version}")
    print(f"  Commit : {commit}")
    print(f"  Tag    : {version}")
    print("\nGitHub Actions will now:")
    print("  - update CHANGELOG.md on tag push")
    print("  - create a GitHub Release with generated notes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
