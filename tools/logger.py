#!/usr/bin/env python3
"""
Author: WOJTEK885

Provides a colored console logger and a small ProjectConfig reader so that
tooling can discover project metadata (name, prefix) from .hemtt/project.toml.
"""

import logging
import sys
import tomllib
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path

_COLORS = {
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
}
_RESET = "\033[0m"


class _ColoredFormatter(logging.Formatter):
    """Formats log records with ANSI colors matching the severity level."""

    def format(self, record: logging.LogRecord) -> str:
        prefix = _COLORS.get(record.levelname, "")
        message = super().format(record)
        return f"{prefix}{message}{_RESET}"


def setup_logger(name: str = "template") -> logging.Logger:
    """Configures and returns the shared project logger with colored output."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(_ColoredFormatter("[%(levelname)s] %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


logger = setup_logger()


class LogLevel(IntEnum):
    """Log levels compatible with the logging module."""

    INFO = logging.INFO
    WARN = logging.WARNING
    ERROR = logging.ERROR


@dataclass(frozen=True)
class ProjectConfig:
    """Metadata read from the project's .hemtt/project.toml file."""

    name: str
    prefix: str
    root: Path
    author: str

    @classmethod
    def discover(cls, start: Path | None = None) -> "ProjectConfig":
        """Locate .hemtt/project.toml by walking up from the given directory.

        Searches from `start` (defaults to the current working directory)
        towards the filesystem root so tools work from the project root, the
        tools/ directory, or any subdirectory.
        """
        current = Path(start or Path.cwd()).resolve()
        for directory in [current] + list(current.parents):
            project_file = directory / ".hemtt" / "project.toml"
            if project_file.exists():
                return cls.from_file(project_file)
        raise FileNotFoundError(
            "Could not locate .hemtt/project.toml in this directory or any parent."
        )

    @classmethod
    def from_file(cls, project_file: Path) -> "ProjectConfig":
        """Read project metadata from an existing .hemtt/project.toml."""
        with open(project_file, "rb") as fh:
            data = tomllib.load(fh)
        return cls(
            name=data["name"],
            prefix=data["prefix"],
            root=project_file.parent.parent,
            author=data.get("author", ""),
        )

    @property
    def acronym(self) -> str:
        """Acronym (uppercase of the prefix)"""
        return self.prefix.upper()


def _config() -> ProjectConfig:
    cached = getattr(_config, "_cached", None)
    if cached is None:
        cached = ProjectConfig.discover()
        _config._cached = cached
    return cached


def log(level: LogLevel, message: str) -> None:
    """Log a message at the given severity."""
    logger.log(level.value, message)


def project_root() -> str:
    """Return the repository root."""
    return str(_config().root)


def get_prefix() -> str:
    """Read the main prefix from .hemtt/project.toml."""
    return _config().prefix


def get_acronym() -> str:
    """Read the main acronym (uppercase of the prefix) from .hemtt/project.toml."""
    return _config().acronym


def get_project_name() -> str:
    """Read the project name from .hemtt/project.toml."""
    return _config().name
