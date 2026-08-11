"""
------------------------------------------------------------
File Name : health_card.py

Purpose:
Displays the overall health of the eSim Companion
software environment.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import customtkinter as ctk

from gui.components.base_card import BaseCard
from utils.theme import Theme


class HealthCard(BaseCard):
    """Displays the overall environment health."""

    def __init__(self, parent, installed, total):

        super().__init__(parent)

        self.installed = installed
        self.total = total

        self.create_widgets()

    def create_widgets(self):
        """Create the health card UI."""

        percentage = self.calculate_percentage()

        if percentage >= 80:
            status = "Excellent"
            status_color = Theme.Colors.SUCCESS

        elif percentage >= 50:
            status = "Needs Attention"
            status_color = Theme.Colors.WARNING

        else:
            status = "Critical"
            status_color = Theme.Colors.ERROR

        # Title
        title = ctk.CTkLabel(
            self,
            text="Environment Health",
            font=Theme.Fonts.HEADING,
            text_color=Theme.Colors.TEXT
        )

        title.pack(
            anchor="w",
            padx=Theme.Spacing.MEDIUM,
            pady=(15, 5)
        )

        # Health information
        info = ctk.CTkLabel(
            self,
            text=f"{self.installed} of {self.total} tools available",
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        info.pack(
            anchor="w",
            padx=Theme.Spacing.MEDIUM
        )

        # Progress bar
        progress = ctk.CTkProgressBar(
            self,
            height=12,
            corner_radius=6,
            progress_color=status_color
        )

        progress.pack(
            fill="x",
            padx=Theme.Spacing.MEDIUM,
            pady=10
        )

        progress.set(percentage / 100)

        # Status
        status_label = ctk.CTkLabel(
            self,
            text=f"{percentage}%  •  {status}",
            font=Theme.Fonts.BODY,
            text_color=status_color
        )

        status_label.pack(
            anchor="w",
            padx=Theme.Spacing.MEDIUM
        )

    def calculate_percentage(self):
        """Calculate the environment health percentage."""

        if self.total == 0:
            return 0

        return round(
            (self.installed / self.total) * 100
        )