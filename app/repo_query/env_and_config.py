"""Environment variables and configuration."""
import json


def load_config(config_file):
    """Load configuration from a file."""
    with open(config_file, "r", encoding="utf-8") as config_file:
        return json.load(config_file)
