from __future__ import annotations

from typing import cast, TypedDict

import tomllib
import os

__all__ = ("Config", "load_config")


class Config(TypedDict):
    """Config structure."""

    host: str
    port: int
    database: str
    username: str
    password: str


def load_config(path: str) -> Config:
    """Load config from a file.

    :param path: Path to the config file.
    :type path: str

    :return: Config structure.
    :rtype: Config

    :raises FileNotFoundError: If the config file does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    try:
        with open(path, "rb") as fp:
            return cast(Config, tomllib.load(fp))
    except Exception as e:
        raise ValueError(f"Failed to parse config file: {path}") from e
