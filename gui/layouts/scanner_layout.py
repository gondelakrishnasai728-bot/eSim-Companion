"""
------------------------------------------------------------
File Name : scanner_layout.py

Purpose:
Provides the detailed environment scanner interface.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import customtkinter as ctk

from services.dependency_checker import DependencyChecker
from gui.components.base_card import BaseCard
from utils.theme import Theme


class ScannerLayout(ctk.CTkFrame):
    """Detailed environment scanner page."""

    def __init__(self, parent, on_scan_complete=None):
        super().__init__(
            master=parent,
            fg_color=Theme.Colors.BACKGROUND
        )

        self.results = []
        self.on_scan_complete = on_scan_complete

        self.create_layout()

    def create_layout(self):
        """Create the scanner interface."""

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
            text="Environment Scanner",
            font=Theme.Fonts.TITLE,
            text_color=Theme.Colors.TEXT
        )

        title.pack(
            side="left"
        )

        self.scan_button = ctk.CTkButton(
            header,
            text="Scan Now",
            width=130,
            height=38,
            command=self.run_scan
        )

        self.scan_button.pack(
            side="right"
        )

        # -------------------------------------------------
        # Description
        # -------------------------------------------------
        description = ctk.CTkLabel(
            self,
            text=(
                "Scan your system for required eSim tools "
                "and check their compatibility."
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
        # Results area
        # -------------------------------------------------
        self.results_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.results_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # -------------------------------------------------
        # Initial message
        # -------------------------------------------------
        self.message_label = ctk.CTkLabel(
            self.results_frame,
            text="Click 'Scan Now' to check your environment.",
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        self.message_label.pack(
            pady=50
        )

    def run_scan(self):
        """Run the dependency scan."""

        self.scan_button.configure(
            text="Scanning...",
            state="disabled"
        )

        checker = DependencyChecker()

        self.results = checker.check_all()
        if self.on_scan_complete:
            self.on_scan_complete(self.results)

        self.display_results()

        self.scan_button.configure(
            text="Scan Now",
            state="normal"
        )

    def display_results(self):
        """Display dependency scan results."""

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        for result in self.results:

            card = BaseCard(
                self.results_frame
            )

            card.pack(
                fill="x",
                padx=5,
                pady=8
            )

            # Tool name
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

            # Version
            version = ctk.CTkLabel(
                card,
                text=f"Version : {result.version or 'Not detected'}",
                font=Theme.Fonts.BODY,
                text_color=Theme.Colors.SUBTEXT
            )

            version.pack(
                anchor="w",
                padx=20
            )

            # Path
            path = ctk.CTkLabel(
                card,
                text=f"Path : {result.path or 'Not available'}",
                font=Theme.Fonts.BODY,
                text_color=Theme.Colors.SUBTEXT
            )

            path.pack(
                anchor="w",
                padx=20,
                pady=(5, 0)
            )

            # Status color
            if result.status == "Installed":
                status_color = Theme.Colors.SUCCESS

            elif result.status == "Incompatible":
                status_color = Theme.Colors.WARNING

            else:
                status_color = Theme.Colors.ERROR

            # Status
            status = ctk.CTkLabel(
                card,
                text=f"Status : {result.status}",
                font=Theme.Fonts.BODY,
                text_color=status_color
            )

            status.pack(
                anchor="w",
                padx=20,
                pady=(10, 5)
            )

            # Message
            message = ctk.CTkLabel(
                card,
                text=result.message,
                font=Theme.Fonts.BODY,
                text_color=Theme.Colors.SUBTEXT
            )

            message.pack(
                anchor="w",
                padx=20,
                pady=(0, 15)
            )