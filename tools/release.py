#!/usr/bin/env python3
"""
Author: WOJTEK885

Creates a release by orchestrating the HEMTT toolchain. By default bumps the
minor version and resets the patch number. Flags allow bumping the major or
patch numbers instead, or skipping the bump / the release entirely.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

from logger import ProjectConfig, logger

_SKIP_FLAG_QC = "skipwhenmissingdependencies = 1"
_LOADORDER_ANCHOR = "_loadorder"


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

    def collect_addons(self, prefix: str) -> list[str]:
        """Return addons eligible for the loadorder, in directory order."""
        addons_dir = self.root / "addons"
        addons: list[str] = []
        if not addons_dir.is_dir():
            return addons

        for folder in sorted(os.listdir(addons_dir)):
            addon_dir = addons_dir / folder
            if not addon_dir.is_dir():
                continue
            if folder.lower() == "loadorder":
                continue

            config_path = addon_dir / "config.cpp"
            content = ""
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read().lower()

            if _SKIP_FLAG_QC in content:
                continue
            if f"{prefix}{_LOADORDER_ANCHOR}" in content:
                continue
            addons.append(folder)

        return addons

    def write_loadorder(self, prefix: str, addons: list[str]) -> int:
        """Write the loadorder addons.hpp. Returns the number of addons written."""
        loadorder_dir = self.root / "addons" / "loadorder"
        if not addons:
            logger.warning("No addons found for loadorder!")
            return 0
        if not loadorder_dir.is_dir():
            logger.warning("No loadorder addon found, skipping")
            return 0

        lines = [f'"{prefix}_{addon}",\n' for addon in addons]
        with open(loadorder_dir / "addons.hpp", "w", encoding="utf-8") as fh:
            fh.writelines(lines)
        return len(addons)

    def sort_loadorder(self) -> None:
        """Sort the loadorder via HEMTT's link subcommand."""
        logger.info("Sorting loadorder")
        self._run(["hemtt", "ln", "sort"])

    def run_config_style_check(self) -> int:
        """Run the separate config style checker process; returns its error count."""
        logger.info("Validating config style")
        script = self.root / "tools" / "config_style_checker.py"
        result = self._run([sys.executable, str(script)])
        return result.returncode

    def release(self, skip: bool) -> bool:
        """Run the HEMTT release build."""
        if skip:
            logger.warning("Skipping release build (--skip-release)")
            return True
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
    parser.add_argument(
        "--skip-release",
        action="store_true",
        help="Do not run the HEMTT release build.",
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

    addons = tool.collect_addons(config.prefix)
    count = tool.write_loadorder(config.prefix, addons)
    logger.info(f"Wrote {count} addons to addons/loadorder/addons.hpp")

    tool.sort_loadorder()

    if tool.run_config_style_check() != 0:
        logger.error("Config validation FAILED; fix the errors and try again.")
        return 1

    if not tool.release(args.skip_release):
        logger.error("HEMTT release failed.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
