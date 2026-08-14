"""
------------------------------------------------------------
File Name : activity_layout.py

Purpose:
Displays the activity history of eSim Companion.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import customtkinter as ctk

from utils.theme import Theme
from gui.components.base_card import BaseCard
from services.activity_manager import ActivityManager

class ActivityLayout(ctk.CTkFrame):
    """Displays application activity history."""

    def __init__(self, parent, activities=None):
        super().__init__(
            master=parent,
            fg_color=Theme.Colors.BACKGROUND
        )

        if activities is None:
            self.activities = ActivityManager.get_activities()
        else:
            self.activities = activities

        self.create_layout()

    def create_layout(self):
        """Create the Activity page."""

        # -------------------------------------------------
        # Header
        # -------------------------------------------------

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        title = ctk.CTkLabel(
            header,
            text="Activity",
            font=Theme.Fonts.TITLE,
            text_color=Theme.Colors.TEXT
        )

        title.pack(
            side="left"
        )

        clear_button = ctk.CTkButton(
            header,
            text="Clear Activity",
            width=130,
            height=36,
            command=self.clear_activity
        )

        clear_button.pack(
            side="right"
        )

        # -------------------------------------------------
        # Description
        # -------------------------------------------------

        description = ctk.CTkLabel(
            self,
            text="View recent eSim Companion activity.",
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        description.pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        # -------------------------------------------------
        # Activity container
        # -------------------------------------------------

        self.activity_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.activity_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.load_activity()

    def load_activity(self):
        """Display the current activity list."""

        for widget in self.activity_frame.winfo_children():
            widget.destroy()

        if not self.activities:
            self.create_empty_state()
            return

        for activity in self.activities:
            self.create_activity_card(activity)

    def create_activity_card(self, activity):
        """Create one activity card."""

        card = BaseCard(
            self.activity_frame
        )

        card.pack(
            fill="x",
            padx=5,
            pady=6
        )

        label = ctk.CTkLabel(
            card,
            text=f"•  {activity}",
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT,
            anchor="w"
        )

        label.pack(
            fill="x",
            padx=20,
            pady=15
        )

    def create_empty_state(self):
        """Display an empty activity message."""

        label = ctk.CTkLabel(
            self.activity_frame,
            text="No activity recorded yet.",
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        label.pack(
            pady=40
        )

    def update_activities(self, activities):
        """Update the displayed activity list."""

        self.activities = activities or []

        self.load_activity()

    def clear_activity(self):
        """Clear the activity history."""

        ActivityManager.clear_activity()

        self.activities = []

        self.load_activity()