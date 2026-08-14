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
from gui.layouts.updates_layout import UpdatesLayout
from gui.layouts.sidebar import Sidebar
from gui.layouts.topbar import TopBar
from gui.layouts.dashboard_layout import DashboardLayout
from gui.layouts.scanner_layout import ScannerLayout
from gui.layouts.tools_layout import ToolsLayout
from gui.layouts.configure_layout import ConfigureLayout
from services.activity_manager import ActivityManager
from gui.layouts.activity_layout import ActivityLayout

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

        self.activity_history = []

        self.run_dependency_scan()

        self.create_layout()

    # -------------------------------------------------
    # Dependency Scan
    # -------------------------------------------------

    def run_dependency_scan(self):
        """Run the dependency checker and record activity."""

        checker = DependencyChecker()

        results = checker.check_all()

        self.tool_results = [
            result_to_card_data(result)
            for result in results
        ]

        ActivityManager.clear_activity()

        ActivityManager.add_activity(
            "Environment scan completed"
        )

        for tool in self.tool_results:

            if tool["installed"]:

                ActivityManager.add_activity(
                    f"{tool['name']} detected"
                )

            else:

                ActivityManager.add_activity(
                    f"{tool['name']} not found"
                )

    # -------------------------------------------------
    # Main Layout
    # -------------------------------------------------

    def create_layout(self):
        """Create the main application layout."""

        self.sidebar = Sidebar(
            self,
            on_navigate=self.handle_navigation
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

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

        self.topbar = TopBar(
            self.content
        )

        self.topbar.pack(
            fill="x"
        )

        self.show_dashboard()

    # -------------------------------------------------
    # Navigation
    # -------------------------------------------------

    def handle_navigation(self, page):
        """Handle sidebar navigation."""

        if page == "dashboard":

            self.show_dashboard()

        elif page == "scanner":

            self.show_scanner()

        elif page == "tools":

            self.show_tools()

        elif page == "configure":

            self.show_configure()

        elif page == "updates":

            self.show_updates()

        elif page == "activity":

            self.show_activity()

        else:

            print(
                f"Page '{page}' is not implemented yet."
            )

    def show_configure(self):
        """Display the configuration page."""

        self.clear_content()

        self.configure_page = ConfigureLayout(
            self.content
        )

        self.configure_page.pack(
            fill="both",
            expand=True
        )

    # -------------------------------------------------
    # Clear Content
    # -------------------------------------------------

    def clear_content(self):
        """Remove the current page while keeping the top bar."""

        for widget in self.content.winfo_children():

            if widget != self.topbar:

                widget.destroy()

    # -------------------------------------------------
    # Dashboard
    # -------------------------------------------------

    def show_dashboard(self):
        """Display the dashboard page."""

        self.clear_content()

        self.dashboard = DashboardLayout(
            self.content
        )

        self.dashboard.pack(
            fill="both",
            expand=True
        )

        installed_count = sum(
            1
            for tool in self.tool_results
            if tool["installed"]
        )

        total_count = len(
            self.tool_results
        )

        self.dashboard.update_health(
            installed_count,
            total_count
        )

        activities = list(
            self.activity_history
        )

        if not activities:

            activities.append(
                "Environment scan completed"
            )

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

        self.add_status_cards()

    # -------------------------------------------------
    # Status Cards
    # -------------------------------------------------

    def add_status_cards(self):
        """Add tool status cards to the dashboard."""

        for index, tool in enumerate(
            self.tool_results
        ):

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

    # -------------------------------------------------
    # Scanner
    # -------------------------------------------------

    def show_scanner(self):
        """Display the environment scanner page."""

        self.clear_content()

        self.scanner = ScannerLayout(
            self.content,
            on_scan_complete=self.handle_scan_complete
        )

        self.scanner.pack(
            fill="both",
            expand=True
        )

    def show_tools(self):
        """Display the tool manager page."""

        self.clear_content()

        self.tools = ToolsLayout(
            self.content,
            on_scan_complete=self.handle_scan_complete
        )

        self.tools.pack(
            fill="both",
            expand=True
        )

    # -------------------------------------------------
    # Scanner Callback
    # -------------------------------------------------

    def handle_scan_complete(self, results):
        """Handle fresh results returned by a dependency scan."""

        self.tool_results = [
            result_to_card_data(result)
            for result in results
        ]

        self.activity_history.append(
            "Environment scan completed"
        )

    # -------------------------------------------------
    # Updates
    # -------------------------------------------------

    def show_updates(self):
        """Display the updates page."""

        self.clear_content()

        self.updates_page = UpdatesLayout(
            self.content
        )

        self.updates_page.pack(
            fill="both",
            expand=True
        )

    # -------------------------------------------------
    # Activity
    # -------------------------------------------------

    def show_activity(self):
        """Display the activity page."""

        self.clear_content()

        self.activity_page = ActivityLayout(
            self.content
        )

        self.activity_page.pack(
            fill="both",
            expand=True
        )


def create_application():
    """Create and configure the application."""

    ctk.set_appearance_mode(
        "Dark"
    )

    ctk.set_default_color_theme(
        "blue"
    )

    return MainWindow()