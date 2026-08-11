"""
------------------------------------------------------------
File Name : main_window.py

Purpose:
Creates and manages the main eSim Companion application
window.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import customtkinter as ctk

from utils.theme import Theme
from gui.layouts.sidebar import Sidebar
from gui.layouts.topbar import TopBar
from gui.layouts.dashboard_layout import DashboardLayout
from gui.components.status_card import StatusCard


class MainWindow(ctk.CTk):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.title(Theme.Window.TITLE)

        self.geometry(
            f"{Theme.Sizes.WINDOW_WIDTH}x"
            f"{Theme.Sizes.WINDOW_HEIGHT}"
        )

        self.minsize(
            Theme.Window.MIN_WIDTH,
            Theme.Window.MIN_HEIGHT
        )

        self.configure(
            fg_color=Theme.Colors.BACKGROUND
        )

        self.create_layout()

    def create_layout(self):
        """Create the main application layout."""

        # Sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # Main content area
        self.content = ctk.CTkFrame(
            self,
            fg_color=Theme.Colors.BACKGROUND,
            corner_radius=0
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Top bar
        self.topbar = TopBar(self.content)
        self.topbar.pack(
            fill="x"
        )

        # Dashboard
        self.dashboard = DashboardLayout(self.content)
        self.dashboard.pack(
            fill="both",
            expand=True
        )

        self.add_status_cards()

    def add_status_cards(self):
        """Add initial tool status cards."""

        tools = [
            {
                "name": "🐍 Python",
                "version": "3.12.10",
                "status": "Installed"
            },
            {
                "name": "🌿 Git",
                "version": "Detected",
                "status": "Installed"
            },
            {
                "name": "⚡ Ngspice",
                "version": "Not Checked",
                "status": "Missing"
            },
            {
                "name": "🛠 KiCad",
                "version": "Not Checked",
                "status": "Missing"
            }
        ]

        for index, tool in enumerate(tools):

            card = StatusCard(
                self.dashboard.cards_frame,
                title=tool["name"],
                version=tool["version"],
                status=tool["status"]
            )

            row = index // 2
            column = index % 2

            card.grid(
                row=row,
                column=column,
                padx=12,
                pady=12,
                sticky="nsew"
            )

        self.dashboard.cards_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.dashboard.cards_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.dashboard.cards_frame.grid_rowconfigure(
            0,
            weight=1
        )

        self.dashboard.cards_frame.grid_rowconfigure(
            1,
            weight=1
        )


def create_application():
    """Create and configure the application."""

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    return MainWindow()