"""
------------------------------------------------------------
File Name : dashboard_layout.py

Purpose:
Creates and manages the main dashboard layout.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import customtkinter as ctk

from utils.theme import Theme
from gui.components.health_card import HealthCard
from gui.components.activity_panel import ActivityPanel


class DashboardLayout(ctk.CTkFrame):
    """Main dashboard layout."""

    def __init__(self, parent):
        super().__init__(
            master=parent,
            fg_color=Theme.Colors.BACKGROUND
        )

        self.create_layout()

    def create_layout(self):
        """Create the dashboard sections."""

        # Environment Health
        self.health_card = HealthCard(
            self,
            installed=2,
            total=4
        )

        self.health_card.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        # Tool Cards Area
        self.cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.cards_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # Recent Activity
        activities = [
            "Application started",
            "Python environment detected",
            "Git environment detected",
            "Dependency scan pending"
        ]

        self.activity_panel = ActivityPanel(
            self,
            activities=activities
        )

        self.activity_panel.pack(
            fill="x",
            padx=20,
            pady=(10, 20)
        )

    def update_health(self, installed, total):
        """Update the environment health card."""
        self.health_card.update_health(
            installed,
            total
        )

        
        self.health_card.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

    def update_activity(self, activities):
        """Update the existing activity panel."""

        self.activity_panel.update_activities(
            activities
        )