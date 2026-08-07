"""
------------------------------------------------------------
File Name : topbar.py

Purpose :
Creates the top navigation bar for the application.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import customtkinter as ctk

from utils.theme import Theme
from utils.constants import AppInfo


class TopBar(ctk.CTkFrame):
    """Top navigation bar."""

    def __init__(self, parent):

        super().__init__(
            master=parent,
            fg_color=Theme.Colors.CARD,
            height=70,
            corner_radius=0,
        )

        self.pack_propagate(False)

        self.create_widgets()

    def create_widgets(self):

        # Left Side
        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=Theme.Fonts.TITLE,
            text_color=Theme.Colors.TEXT,
        )

        title.pack(side="left", padx=25)

        # Right Side
        version = ctk.CTkLabel(
            self,
            text=f"{AppInfo.NAME}  v{AppInfo.VERSION}",
            font=Theme.Fonts.SMALL,
            text_color=Theme.Colors.SUBTEXT,
        )

        version.pack(side="right", padx=25)