"""Utility functions for the application."""
import json
import os
import re
from typing import List


def load_string_from_file(file_path: str) -> str:
    """Load a string from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()


def check_env_vars(env_vars: List[str]) -> None:
    """Check if environment variables are set."""
    for var in env_vars:
        if var not in os.environ:
            raise EnvironmentError(f"Environment variable {var} not set")


def load_config(file_path: str) -> dict:
    """Load a configuration file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def is_valid_folder_name(folder_name: str) -> bool:
    """
    Check if a given folder name is valid.
    """
    # Regular expression to match against any character not allowed in a folder name
    if re.search(r'[<>:"/\\|?*]', folder_name):
        return False

    # Checking for names reserved by Windows
    # even though they are not reserved under Unix-like systems
    if folder_name.upper() in (
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    ):
        return False

    # Further checks can be added for other OS specific constraints
    return True
