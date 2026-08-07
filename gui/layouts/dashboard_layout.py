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

        self.health_frame = ctk.CTkFrame(
            self,
            height=120,
            fg_color=Theme.Colors.CARD,
            corner_radius=Theme.Radius.LARGE
        )

        self.health_frame.pack(
            fill="x",
            padx=20,
            pady=(20,10)
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

        self.activity_frame = ctk.CTkFrame(
            self,
            height=150,
            fg_color=Theme.Colors.CARD,
            corner_radius=Theme.Radius.LARGE
        )

        self.activity_frame.pack(
            fill="x",
            padx=20,
            pady=(10,20)
        )