"""
------------------------------------------------------------
File Name : sidebar.py

Purpose:
Creates the left navigation sidebar for
eSim Companion.

Author : Krishna Sai
------------------------------------------------------------
"""

import customtkinter as ctk
from utils.theme import Theme


class Sidebar(ctk.CTkFrame):
    """Application navigation sidebar."""

    def __init__(self, parent):
        super().__init__(
            master=parent,
            width=Theme.Sizes.SIDEBAR_WIDTH,
            fg_color=Theme.Colors.SIDEBAR,
            corner_radius=0
        )

        self.pack_propagate(False)

        self.create_widgets()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="eSim Companion",
            font=Theme.Fonts.TITLE,
            text_color=Theme.Colors.TEXT
        )

        title.pack(pady=(30, 40))

        menu_items = [
            "🏠 Dashboard",
            "🔍 Scanner",
            "📦 Tools",
            "⚙ Configure",
            "🔄 Updates",
            "📜 Activity"
        ]

        for item in menu_items:

            button = ctk.CTkButton(
                self,
                text=item,
                fg_color="transparent",
                hover_color=Theme.Colors.CARD_HOVER,
                anchor="w",
                height=42,
                corner_radius=10,
                font=Theme.Fonts.BODY
            )

            button.pack(
                fill="x",
                padx=15,
                pady=5
            )