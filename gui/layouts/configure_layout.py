"""
------------------------------------------------------------
File Name : configure_layout.py

Purpose:
Provides configuration settings for external eSim tools.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import tkinter.filedialog as filedialog
from pathlib import Path

import customtkinter as ctk

from utils.theme import Theme
from services.dependency_checker import DependencyChecker
from gui.components.base_card import BaseCard
from config.config_manager import ConfigManager


class ConfigureLayout(ctk.CTkFrame):
    """Configuration page for external tools."""

    EXPECTED_EXECUTABLES = {
        "Python": ["python.exe"],
        "Git": ["git.exe"],
        "Ngspice": ["ngspice.exe"],
        "KiCad": ["kicad.exe"],
    }

    def __init__(self, parent):
        super().__init__(
            master=parent,
            fg_color=Theme.Colors.BACKGROUND
        )

        self.create_layout()

    def create_layout(self):
        """Create the configuration page."""

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
            text="Configure",
            font=Theme.Fonts.TITLE,
            text_color=Theme.Colors.TEXT
        )

        title.pack(
            side="left"
        )

        # -------------------------------------------------
        # Description
        # -------------------------------------------------

        description = ctk.CTkLabel(
            self,
            text=(
                "View and configure the paths used by "
                "eSim Companion."
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
        # Configuration container
        # -------------------------------------------------

        self.config_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.config_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.load_configuration()

    def load_configuration(self):
        """Load the detected tool paths."""

        for widget in self.config_frame.winfo_children():
            widget.destroy()

        checker = DependencyChecker()

        results = checker.check_all()

        config = ConfigManager.load_config()

        for result in results:

            if config.get(result.name):
                result.path = config[result.name]

            self.create_tool_config_card(
                result
            )

    def create_tool_config_card(self, result):
        """Create a configuration card for one tool."""

        card = BaseCard(
            self.config_frame
        )

        card.configure(
            height=170
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
        # Status
        # -------------------------------------------------

        status_color = Theme.Colors.SUCCESS

        if result.status == "Missing":

            status_color = Theme.Colors.ERROR

        elif result.status == "Incompatible":

            status_color = Theme.Colors.WARNING

        status = ctk.CTkLabel(
            card,
            text=f"Status : {result.status}",
            font=Theme.Fonts.BODY,
            text_color=status_color
        )

        status.pack(
            anchor="w",
            padx=20
        )

        # -------------------------------------------------
        # Path
        # -------------------------------------------------

        path = ctk.CTkLabel(
            card,
            text=(
                f"Path : "
                f"{result.path or 'Not configured'}"
            ),
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        path.pack(
            anchor="w",
            padx=20,
            pady=(8, 10)
        )

        # -------------------------------------------------
        # Configure button
        # -------------------------------------------------

        configure_button = ctk.CTkButton(
            card,
            text="Configure",
            width=120,
            height=34,
            command=lambda name=result.name:
                self.configure_tool(name)
        )

        configure_button.pack(
            anchor="e",
            padx=20,
            pady=(0, 15)
        )

    def configure_tool(self, tool_name):
        """Allow the user to select and validate a tool executable."""

        file_path = filedialog.askopenfilename(
            title=f"Select {tool_name} executable",
            filetypes=[
                ("Executable files", "*.exe"),
                ("All files", "*.*")
            ]
        )

        if not file_path:
            return

        selected_name = Path(
            file_path
        ).name.lower()

        expected_names = [
            name.lower()
            for name in self.EXPECTED_EXECUTABLES.get(
                tool_name,
                []
            )
        ]

        if selected_name not in expected_names:

            print(
                f"Invalid executable selected for "
                f"{tool_name}: {selected_name}"
            )

            return

        ConfigManager.set_path(
            tool_name,
            file_path
        )

        self.load_configuration()