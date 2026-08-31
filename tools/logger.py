#!/usr/bin/env python3
"""
Author: DartRuffian
Description:
  Handles writing log messages with colored text for different log levels.
  Also provides shared helpers for reading the project's prefix from
  .hemtt/project.toml so tools are not hardcoded to a specific mod.
"""

import os
import tomllib
from enum import Enum


class LogLevel(Enum):
    INFO = "[32m INFO"
    WARN = "[33m WARN"
    ERROR = "[31mERROR"


def log(level: LogLevel, message: str) -> None:
    """Logs a message to stdout with the given level"""
    print(f"\033{level.value}\033[0m {message}")


def project_root() -> str:
    """Return the repository root, allowing tools to run from root or from tools/"""
    cwd = os.getcwd()
    if os.path.basename(cwd) == "tools" and os.path.exists("../.hemtt/project.toml"):
        return os.path.abspath(os.path.join(cwd, ".."))
    return cwd


def get_prefix() -> str:
    """Read the main prefix from .hemtt/project.toml"""
    root = project_root()
    with open(os.path.join(root, ".hemtt", "project.toml"), "rb") as f:
        data = tomllib.load(f)
    return data["prefix"]


def get_project_name() -> str:
    """Read the project name from .hemtt/project.toml"""
    root = project_root()
    with open(os.path.join(root, ".hemtt", "project.toml"), "rb") as f:
        data = tomllib.load(f)
    return data["name"]
