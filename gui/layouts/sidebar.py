"""
------------------------------------------------------------
File Name : sidebar.py

Purpose:
Creates the left navigation sidebar for
eSim Companion.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import customtkinter as ctk

from utils.theme import Theme


class Sidebar(ctk.CTkFrame):
    """Application navigation sidebar."""

    def __init__(self, parent, on_navigate=None):

        super().__init__(
            master=parent,
            width=Theme.Sizes.SIDEBAR_WIDTH,
            fg_color=Theme.Colors.SIDEBAR,
            corner_radius=0
        )

        self.on_navigate = on_navigate

        self.pack_propagate(False)

        self.create_widgets()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="eSim Companion",
            font=Theme.Fonts.TITLE,
            text_color=Theme.Colors.TEXT
        )

        title.pack(
            pady=(30, 40)
        )

        menu_items = [
            ("🏠 Dashboard", "dashboard"),
            ("🔍 Scanner", "scanner"),
            ("📦 Tools", "tools"),
            ("⚙ Configure", "configure"),
            ("🔄 Updates", "updates"),
            ("📜 Activity", "activity")
        ]

        for text, page in menu_items:

            button = ctk.CTkButton(
                self,
                text=text,
                fg_color="transparent",
                hover_color=Theme.Colors.CARD_HOVER,
                anchor="w",
                height=42,
                corner_radius=10,
                font=Theme.Fonts.BODY,
                command=lambda p=page: self.navigate(p)
            )

            button.pack(
                fill="x",
                padx=15,
                pady=5
            )

    def navigate(self, page):
        """Send the selected page to the main window."""

        if self.on_navigate:
            self.on_navigate(page)