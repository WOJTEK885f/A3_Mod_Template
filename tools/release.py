#!/usr/bin/env python3
"""
Author: WOJTEK885

Creates a release by orchestrating the HEMTT toolchain. By default bumps the
minor version and resets the patch number. Flags allow bumping the major or
patch numbers instead, or skipping the bump.
"""

import argparse
import subprocess
import sys
from pathlib import Path

from logger import ProjectConfig, logger


class ReleaseTool:
    """Orchestrates the steps required to produce and verify a release."""

    def __init__(self, config: ProjectConfig) -> None:
        self.config = config
        self.root = config.root

    def _run(self, args: list[str], *, check: bool = False) -> subprocess.CompletedProcess:
        return subprocess.run(args, cwd=self.root, check=check)

    def bump_version(self, kind: str, skip: bool) -> bool:
        """Run the HEMTT script that updates the selected version component."""
        if skip:
            logger.warning("Skipping version bump (--skip-bump)")
            return True
        logger.info(f"Bumping {kind} version")
        script = {
            "major": "update_major.rhai",
            "minor": "update_minor.rhai",
            "patch": "update_patch.rhai",
        }[kind]
        result = self._run(["hemtt", "script", script])
        return result.returncode == 0

    def run_config_style_check(self) -> int:
        """Run the separate config style checker process; returns its error count."""
        logger.info("Validating config style")
        script = self.root / "tools" / "config_style_checker.py"
        result = self._run([sys.executable, str(script)])
        return result.returncode

    def release(self) -> bool:
        """Run the HEMTT release build."""
        logger.info("Running hemtt release")
        result = self._run(["hemtt", "release"])
        return result.returncode == 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a release for the mod.")
    parser.add_argument(
        "--major",
        action="store_true",
        help="Bump the major version and reset minor/patch.",
    )
    parser.add_argument(
        "--patch",
        action="store_true",
        help="Bump only the patch version.",
    )
    parser.add_argument(
        "--skip-bump",
        action="store_true",
        help="Do not bump the version.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    try:
        config = ProjectConfig.discover()
    except FileNotFoundError as exc:
        logger.error(str(exc))
        return 1

    tool = ReleaseTool(config)
    logger.info(f"Project: '{config.name}'")
    logger.info(f"Main Prefix: '{config.prefix}'")

    bump_kind = "major" if args.major else "patch" if args.patch else "minor"
    if not tool.bump_version(bump_kind, args.skip_bump):
        logger.error("Version bump failed.")
        return 1

    if tool.run_config_style_check() != 0:
        logger.error("Config validation FAILED; fix the errors and try again.")
        return 1

    if not tool.release():
        logger.error("HEMTT release failed.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
