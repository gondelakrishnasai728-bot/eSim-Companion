"""
------------------------------------------------------------
File Name : activity_manager.py

Purpose:
Manages persistent application activity history
for eSim Companion.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import json
from pathlib import Path


class ActivityManager:
    """Stores and manages persistent application activity."""

    ACTIVITY_FILE = (
        Path(__file__).parent.parent
        / "logs"
        / "activity.json"
    )

    @classmethod
    def _load(cls):
        """Load activities from the JSON file."""

        if not cls.ACTIVITY_FILE.exists():
            return []

        try:
            with open(
                cls.ACTIVITY_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

        except (
            OSError,
            json.JSONDecodeError
        ):
            pass

        return []

    @classmethod
    def _save(cls, activities):
        """Save activities to the JSON file."""

        cls.ACTIVITY_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            cls.ACTIVITY_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                activities,
                file,
                indent=4
            )

    @classmethod
    def add_activity(cls, message):
        """Add and persist an activity message."""

        if not message:
            return

        activities = cls._load()

        activities.append(message)

        cls._save(activities)

    @classmethod
    def get_activities(cls):
        """Return all saved activities."""

        return cls._load()

    @classmethod
    def clear_activity(cls):
        """Clear all saved activities."""

        cls._save([])