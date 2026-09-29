#!/usr/bin/env python3
"""
Author: WOJTEK885

Creates a release by orchestrating the HEMTT toolchain. By default bumps the
minor version and resets the patch number. Flags allow bumping the major or
patch numbers instead, or skipping the bump.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

from fs_naming import sanitize_windows_name
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

    def ensure_release_folder_safe(self) -> bool:
        """Make `[hemtt.release] folder` Windows-safe before HEMTT reads it.

        HEMTT copies this value verbatim into zip entry names, so a mod name
        containing e.g. ':' would produce an archive that cannot be extracted
        on Windows. Sanitize it and rewrite project.toml when it changed.
        """
        raw = self.config.release_folder
        if raw is None:
            return True

        safe = sanitize_windows_name(raw) or self.config.prefix
        if safe == raw:
            return True

        logger.warning(f"Release folder '{raw}' is not Windows-safe; using '{safe}'")
        if not self._patch_release_folder(safe):
            logger.error("Failed to update [hemtt.release] folder in .hemtt/project.toml.")
            return False
        return True

    def _patch_release_folder(self, safe: str) -> bool:
        """Replace the `folder` value inside the [hemtt.release] table only."""
        project_file = self.root / ".hemtt" / "project.toml"
        try:
            text = project_file.read_text(encoding="utf-8")
        except OSError:
            return False

        lines = text.splitlines(keepends=True)
        in_release = False
        for index, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                in_release = stripped == "[hemtt.release]"
                continue
            if in_release and re.match(r"^\s*folder\s*=", line):
                indent = line[: len(line) - len(line.lstrip())]
                newline = "\n" if line.endswith("\n") else ""
                lines[index] = f'{indent}folder = "{safe}"{newline}'
                project_file.write_text("".join(lines), encoding="utf-8")
                return True
        return False

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

    if not tool.ensure_release_folder_safe():
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
