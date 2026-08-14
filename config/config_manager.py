"""
------------------------------------------------------------
File Name : config_manager.py

Purpose:
Loads and saves external tool paths for eSim Companion.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import json
from pathlib import Path


class ConfigManager:
    """Manages saved tool configuration."""

    CONFIG_FILE = (
        Path(__file__).parent / "tool_paths.json"
    )

    DEFAULT_CONFIG = {
        "Python": None,
        "Git": None,
        "Ngspice": None,
        "KiCad": None
    }

    @classmethod
    def load_config(cls):
        """Load the saved configuration."""

        if not cls.CONFIG_FILE.exists():
            cls.save_config(cls.DEFAULT_CONFIG)
            return cls.DEFAULT_CONFIG.copy()

        try:
            with open(
                cls.CONFIG_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                config = json.load(file)

            return config

        except (
            OSError,
            json.JSONDecodeError
        ):
            return cls.DEFAULT_CONFIG.copy()

    @classmethod
    def save_config(cls, config):
        """Save the configuration."""

        with open(
            cls.CONFIG_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                config,
                file,
                indent=4
            )

    @classmethod
    def get_path(cls, tool_name):
        """Get the configured path for a tool."""

        config = cls.load_config()

        return config.get(tool_name)

    @classmethod
    def set_path(cls, tool_name, path):
        """Save the path for a tool."""

        config = cls.load_config()

        config[tool_name] = path

        cls.save_config(config)