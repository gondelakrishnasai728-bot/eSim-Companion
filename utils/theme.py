"""
------------------------------------------------------------
File Name : theme.py

Purpose:
Defines the complete design system for the
eSim Companion application.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""


class Theme:
    """Central design system for the application."""

    class Colors:
        """Application color palette."""

        BACKGROUND = "#0F172A"
        SIDEBAR = "#111827"
        CARD = "#1E293B"
        CARD_HOVER = "#293548"

        PRIMARY = "#2563EB"
        SECONDARY = "#7C3AED"

        SUCCESS = "#10B981"
        WARNING = "#F59E0B"
        ERROR = "#EF4444"

        TEXT = "#F8FAFC"
        SUBTEXT = "#94A3B8"

        BORDER = "#334155"

    class Fonts:
        """Application fonts."""

        TITLE = ("Segoe UI", 24, "bold")
        HEADING = ("Segoe UI", 18, "bold")
        BODY = ("Segoe UI", 14)
        SMALL = ("Segoe UI", 12)

    class Sizes:
        """Standard UI sizes."""

        SIDEBAR_WIDTH = 220

        BUTTON_HEIGHT = 40

        CARD_WIDTH = 260
        CARD_HEIGHT = 140

        WINDOW_WIDTH = 1400
        WINDOW_HEIGHT = 850

    class Radius:
        """Corner radius values."""

        SMALL = 8
        MEDIUM = 14
        LARGE = 20

    class Spacing:
        """Spacing values."""

        SMALL = 8
        MEDIUM = 16
        LARGE = 24
        XLARGE = 32

    class Animation:
        """Animation timings."""

        SPLASH_DELAY = 2000

    class Window:
        """Application window settings."""

        TITLE = "eSim Companion"

        MIN_WIDTH = 1200
        MIN_HEIGHT = 750