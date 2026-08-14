"""
------------------------------------------------------------
File Name : updates_layout.py

Purpose:
Displays update information for eSim Companion tools.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import customtkinter as ctk

from utils.theme import Theme
from services.dependency_checker import DependencyChecker
from gui.components.base_card import BaseCard


class UpdatesLayout(ctk.CTkFrame):
    """Displays available update information."""

    def __init__(self, parent):
        super().__init__(
            master=parent,
            fg_color=Theme.Colors.BACKGROUND
        )

        self.create_layout()

    def create_layout(self):
        """Create the Updates page."""

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
            text="Updates",
            font=Theme.Fonts.TITLE,
            text_color=Theme.Colors.TEXT
        )

        title.pack(
            side="left"
        )

        self.check_button = ctk.CTkButton(
            header,
            text="Check for Updates",
            width=150,
            height=36,
            command=self.check_updates
        )

        self.check_button.pack(
            side="right"
        )

        # -------------------------------------------------
        # Description
        # -------------------------------------------------

        description = ctk.CTkLabel(
            self,
            text=(
                "Check the installed tools and view "
                "their update status."
            ),
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        description.pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        # -------------------------------------------------
        # Update cards
        # -------------------------------------------------

        self.updates_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.updates_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.load_updates()

    def load_updates(self):
        """Load the current tool information."""

        for widget in self.updates_frame.winfo_children():
            widget.destroy()

        checker = DependencyChecker()

        results = checker.check_all()

        for result in results:
            self.create_update_card(result)

    def create_update_card(self, result):
        """Create an update card for a tool."""

        card = BaseCard(
            self.updates_frame
        )

        card.pack(
            fill="x",
            padx=5,
            pady=8
        )

        # -------------------------------------------------
        # Tool name
        # -------------------------------------------------

        title = ctk.CTkLabel(
            card,
            text=result.name,
            font=Theme.Fonts.HEADING,
            text_color=Theme.Colors.TEXT
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        # -------------------------------------------------
        # Installed version
        # -------------------------------------------------

        version = result.version or "Not installed"

        version_label = ctk.CTkLabel(
            card,
            text=f"Installed Version : {version}",
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        version_label.pack(
            anchor="w",
            padx=20
        )

        # -------------------------------------------------
        # Update status
        # -------------------------------------------------

        if not result.installed:
            status_text = "Not Installed"
            status_color = Theme.Colors.ERROR

        else:
            status_text = "Up to Date"
            status_color = Theme.Colors.SUCCESS

        status_label = ctk.CTkLabel(
            card,
            text=f"Update Status : {status_text}",
            font=Theme.Fonts.BODY,
            text_color=status_color
        )

        status_label.pack(
            anchor="w",
            padx=20,
            pady=(8, 15)
        )

    def check_updates(self):
        """Refresh update information."""

        self.check_button.configure(
            text="Checking...",
            state="disabled"
        )

        self.after(
            300,
            self.finish_update_check
        )

    def finish_update_check(self):
        """Finish the update check."""

        self.load_updates()

        self.check_button.configure(
            text="Check for Updates",
            state="normal"
        )