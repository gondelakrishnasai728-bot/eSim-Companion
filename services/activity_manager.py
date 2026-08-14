"""
------------------------------------------------------------
File Name : activity_manager.py

Purpose:
Manages application activity history for eSim Companion.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""


class ActivityManager:
    """Stores and manages application activity."""

    _activities = []

    @classmethod
    def add_activity(cls, message):
        """Add an activity message."""

        if message:
            cls._activities.append(message)

    @classmethod
    def get_activities(cls):
        """Return all recorded activities."""

        return cls._activities.copy()

    @classmethod
    def clear_activity(cls):
        """Clear all activity history."""

        cls._activities.clear()