"""
------------------------------------------------------------
File Name : dashboard_layout.py

Purpose :
Creates the main dashboard layout that arranges
all dashboard sections.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""
from gui.components.health_card import HealthCard
from gui.components.activity_panel import ActivityPanel
import customtkinter as ctk

from utils.theme import Theme


class DashboardLayout(ctk.CTkFrame):
    """Main dashboard layout."""

    def __init__(self, parent):

        super().__init__(
            master=parent,
            fg_color=Theme.Colors.BACKGROUND
        )

        self.create_layout()

    def create_layout(self):

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