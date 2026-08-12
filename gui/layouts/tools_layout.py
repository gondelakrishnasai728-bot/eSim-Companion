"""
------------------------------------------------------------
File Name : tools_layout.py

Purpose:
Displays the available eSim Companion tools and their
installation status.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import customtkinter as ctk
import webbrowser
import threading

from utils.theme import Theme
from services.dependency_checker import DependencyChecker
from config.tools import TOOLS
from gui.components.base_card import BaseCard


class ToolsLayout(ctk.CTkFrame):
    """Tools management page."""

    def __init__(self, parent,on_scan_complete=None):
        super().__init__(
            master=parent,
            fg_color=Theme.Colors.BACKGROUND
        )
        self.on_scan_complete = on_scan_complete

        self.create_layout()

    def create_layout(self):
        """Create the tools page."""

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
            text="Tool Manager",
            font=Theme.Fonts.TITLE,
            text_color=Theme.Colors.TEXT
        )

        title.pack(
            side="left"
        )
        self.rescan_button = ctk.CTkButton(
            header,
            text="Rescan",
            width=110,
            height=36,
            command=self.rescan
        )

        self.rescan_button.pack(
            side="right"
        )

        # -------------------------------------------------
        # Description
        # -------------------------------------------------

        description = ctk.CTkLabel(
            self,
            text=(
                "View required eSim tools and their "
                "installation status."
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
        # Tools container
        # -------------------------------------------------

        self.tools_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.tools_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.load_tools()

    def load_tools(self):
        """Check and display all configured tools."""

        checker = DependencyChecker()

        results = checker.check_all()

        for result in results:

            self.create_tool_card(
                result
            )

    def create_tool_card(self, result):
        """Create a card for one tool."""

        card = BaseCard(
            self.tools_frame
        )
        card.configure(
            height=210
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
        # Version
        # -------------------------------------------------

        version = ctk.CTkLabel(
            card,
            text=(
                f"Version : "
                f"{result.version or 'Not detected'}"
            ),
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        version.pack(
            anchor="w",
            padx=20
        )

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        if result.status == "Installed":

            status_color = Theme.Colors.SUCCESS

        elif result.status == "Incompatible":

            status_color = Theme.Colors.WARNING

        else:

            status_color = Theme.Colors.ERROR

        status = ctk.CTkLabel(
            card,
            text=f"Status : {result.status}",
            font=Theme.Fonts.BODY,
            text_color=status_color
        )

        status.pack(
            anchor="w",
            padx=20,
            pady=(8, 0)
        )

        # -------------------------------------------------
        # Path
        # -------------------------------------------------

        path = ctk.CTkLabel(
            card,
            text=(
                f"Path : "
                f"{result.path or 'Not available'}"
            ),
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        path.pack(
            anchor="w",
            padx=20,
            pady=(5, 0)
        )

        # -------------------------------------------------
        # Action
        # -------------------------------------------------

        if result.status == "Missing":

            action_button = ctk.CTkButton(
                card,
                text="Install",
                width=110,
                height=34,
                command=lambda name=result.name:
                    self.install_tool(name)
            )

            action_button.pack(
                anchor="e",
                padx=20,
                pady=(5, 15)
            )

        else:

            action_button = ctk.CTkButton(
                card,
                text="Installed",
                width=110,
                height=34,
                state="disabled"
            )

            action_button.pack(
                anchor="e",
                padx=20,
                pady=(5, 15)
            )

    def install_tool(self, tool_name):
        """Open the official download page for a missing tool."""

        download_pages = {
            "Ngspice": "https://sourceforge.net/projects/ngspice/files/ng-spice-rework/",
            "KiCad": "https://www.kicad.org/download/",
        }

        url = download_pages.get(tool_name)

        if url:
            webbrowser.open(url)
    def rescan(self):
        """Start a background dependency scan."""

        self.rescan_button.configure(
            text="Scanning...",
            state="disabled"
        )

        thread = threading.Thread(
            target=self._perform_rescan,
            daemon=True
        )

        thread.start()


    def _perform_rescan(self):
        """Perform the dependency scan in the background."""

        checker = DependencyChecker()

        results = checker.check_all()

        self.after(
            0,
            lambda: self._display_rescan_results(results)
        )


    def _display_rescan_results(self, results):
        """Update the UI with fresh scan results."""

        for widget in self.tools_frame.winfo_children():
            widget.destroy()

        for result in results:
            self.create_tool_card(result)
        if self.on_scan_complete:
            self.on_scan_complete(results)

        self.rescan_button.configure(
            text="Rescan",
            state="normal"
        )