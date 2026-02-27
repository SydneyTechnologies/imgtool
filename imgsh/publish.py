from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

BUMP_RULES = ("patch", "minor", "major", "prepatch", "preminor", "premajor", "prerelease")


def _run(command: list[str]) -> None:
    print(f"+ {' '.join(command)}", flush=True)
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def _run_capture(command: list[str]) -> str:
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"+ {' '.join(command)}", flush=True)
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="")
        raise SystemExit(result.returncode)
    return result.stdout.strip()


def _ensure_clean_worktree() -> None:
    status = _run_capture(["git", "status", "--porcelain"])
    if status:
        raise SystemExit(
            "Git working tree is not clean. Commit/stash changes before running publish."
        )


def _ensure_tag_not_exists(tag: str) -> None:
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode == 0:
        raise SystemExit(f"Tag already exists: {tag}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="publish",
        description="Bump version and create a release tag.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--bump", choices=BUMP_RULES, default="patch", help="Version bump rule.")
    group.add_argument("--version", type=str, help="Set an explicit version.")
    parser.add_argument("--push", action="store_true", help="Push commit and tag to remote.")
    parser.add_argument("--remote", type=str, default="origin", help="Git remote for --push.")
    return parser


def run() -> None:
    args = _build_parser().parse_args()
    _ensure_clean_worktree()

    current_version = _run_capture(["poetry", "version", "--short"])
    if args.version:
        new_version = _run_capture(["poetry", "version", args.version, "--short"])
    else:
        new_version = _run_capture(["poetry", "version", args.bump, "--short"])

    if new_version == current_version:
        raise SystemExit(f"Version was not updated (still {current_version}).")

    tag = f"v{new_version}"
    _ensure_tag_not_exists(tag)

    files_to_add = ["pyproject.toml"]
    if Path("poetry.lock").exists():
        files_to_add.append("poetry.lock")
    _run(["git", "add", *files_to_add])
    _run(["git", "commit", "-m", f"chore(release): {tag}"])
    _run(["git", "tag", tag])

    print(f"Created release tag: {tag}", flush=True)
    if args.push:
        _run(["git", "push", args.remote, "HEAD"])
        _run(["git", "push", args.remote, tag])
    else:
        print(
            f"Next step: git push {args.remote} HEAD && git push {args.remote} {tag}",
            flush=True,
        )


if __name__ == "__main__":
    run()
