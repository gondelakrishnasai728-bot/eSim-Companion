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
from services.dependency_checker import DependencyChecker
from gui.components.tool_mapper import result_to_card_data

from utils.theme import Theme
from gui.layouts.sidebar import Sidebar
from gui.layouts.topbar import TopBar
from gui.layouts.dashboard_layout import DashboardLayout
from gui.components.status_card import StatusCard


class MainWindow(ctk.CTk):
    """Main application window."""
    def run_dependency_scan(self):
        """Run the dependency checker and store the results."""

        checker = DependencyChecker()

        results = checker.check_all()

        self.tool_results = [
            result_to_card_data(result)
            for result in results
        ]

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

        # Run dependency scan first
        self.run_dependency_scan()

        # -------------------------------------------------
        # Sidebar
        # -------------------------------------------------
        self.sidebar = Sidebar(self)

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # -------------------------------------------------
        # Main content area
        # -------------------------------------------------
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

        # -------------------------------------------------
        # Top bar
        # -------------------------------------------------
        self.topbar = TopBar(self.content)

        self.topbar.pack(
            fill="x"
        )

        # -------------------------------------------------
        # Dashboard
        # -------------------------------------------------
        self.dashboard = DashboardLayout(
            self.content
        )

        self.dashboard.pack(
            fill="both",
            expand=True
        )

        # -------------------------------------------------
        # Calculate environment health
        # -------------------------------------------------
        installed_count = sum(
            1
            for tool in self.tool_results
            if tool["installed"]
        )

        total_count = len(self.tool_results)

        self.dashboard.update_health(
            installed_count,
            total_count
        )

        # -------------------------------------------------
        # Create activity messages
        # -------------------------------------------------
        activities = [
            "Environment scan completed"
        ]

        for tool in self.tool_results:

            if tool["installed"]:
                activities.append(
                    f"{tool['name']} detected"
                )
            else:
                activities.append(
                    f"{tool['name']} not found"
                )

        self.dashboard.update_activity(
            activities
        )

        # -------------------------------------------------
        # Add tool cards
        # -------------------------------------------------
        self.add_status_cards()
        

    def add_status_cards(self):
        """Add initial tool status cards."""

        tools = self.tool_results

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