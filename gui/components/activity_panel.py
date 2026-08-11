"""
------------------------------------------------------------
File Name : activity_panel.py

Purpose:
Displays recent actions and events performed by
eSim Companion.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import customtkinter as ctk

from gui.components.base_card import BaseCard
from utils.theme import Theme


class ActivityPanel(BaseCard):
    """Displays recent application activity."""

    def __init__(self, parent, activities=None):

        super().__init__(parent)

        self.activities = activities or []

        self.create_widgets()

    def create_widgets(self):
        """Create the activity panel UI."""

        title = ctk.CTkLabel(
            self,
            text="Recent Activity",
            font=Theme.Fonts.HEADING,
            text_color=Theme.Colors.TEXT
        )

        title.pack(
            anchor="w",
            padx=Theme.Spacing.MEDIUM,
            pady=(15, 5)
        )

        if not self.activities:
            empty_label = ctk.CTkLabel(
                self,
                text="No recent activity",
                font=Theme.Fonts.BODY,
                text_color=Theme.Colors.SUBTEXT
            )

            empty_label.pack(
                anchor="w",
                padx=Theme.Spacing.MEDIUM,
                pady=10
            )

            return

        for activity in self.activities:

            activity_label = ctk.CTkLabel(
                self,
                text=f"●  {activity}",
                font=Theme.Fonts.BODY,
                text_color=Theme.Colors.SUBTEXT
            )

            activity_label.pack(
                anchor="w",
                padx=Theme.Spacing.MEDIUM,
                pady=3
            )
            
    def update_activities(self, activities):
        """Update the displayed activity list."""

        self.activities = activities

        for widget in self.winfo_children():
            widget.destroy()

        self.create_widgets()