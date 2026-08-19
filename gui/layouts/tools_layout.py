"""
------------------------------------------------------------
File Name : tools_layout.py

Purpose:
Display and manage external eSim tools.

Features:
- Automatic dependency scanning
- Installed version detection
- Latest version detection
- Automatic installation
- Automatic updates
- Ngspice official-release update
- Python WinGet version-line checking
- Action logging
- Background operations to keep the GUI responsive

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import re
import subprocess
import threading
from datetime import datetime

import customtkinter as ctk

from utils.theme import Theme
from services.dependency_checker import DependencyChecker
from services.tool_installer import ToolInstaller
from services.update_checker import UpdateChecker
from gui.components.base_card import BaseCard


class ToolsLayout(ctk.CTkFrame):
    """Automated tool management page."""

    def __init__(
        self,
        parent,
        on_scan_complete=None
    ):
        super().__init__(
            master=parent,
            fg_color=Theme.Colors.BACKGROUND
        )

        self.on_scan_complete = on_scan_complete

        self.scanning = False
        self.installing = False
        self.updating = False

        self.results = []
        self.latest_versions = {}

        self.create_layout()

        # -------------------------------------------------
        # Automatically scan when the page is created.
        # -------------------------------------------------

        self.after(
            100,
            self.rescan
        )

    # =====================================================
    # Layout
    # =====================================================

    def create_layout(self):
        """Create the Tool Manager interface."""

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
                "Automatically scan, install, update, "
                "and manage required eSim tools."
            ),
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        description.pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
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
            pady=(5, 5)
        )

        # -------------------------------------------------
        # Action log
        # -------------------------------------------------

        log_title = ctk.CTkLabel(
            self,
            text="Action Log",
            font=Theme.Fonts.HEADING,
            text_color=Theme.Colors.TEXT
        )

        log_title.pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        self.log_box = ctk.CTkTextbox(
            self,
            height=130,
            wrap="word"
        )

        self.log_box.pack(
            fill="x",
            padx=25,
            pady=(0, 15)
        )

        self.log_box.configure(
            state="disabled"
        )

    # =====================================================
    # Logging
    # =====================================================

    def log_action(self, message):
        """Write an action to the visible action log."""

        if not self.winfo_exists():
            return

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        entry = (
            f"[{timestamp}] "
            f"{message}\n"
        )

        self.log_box.configure(
            state="normal"
        )

        self.log_box.insert(
            "end",
            entry
        )

        self.log_box.see(
            "end"
        )

        self.log_box.configure(
            state="disabled"
        )

    # =====================================================
    # Load tools
    # =====================================================

    def load_tools(self, results):
        """Display dependency scan results."""

        if not self.winfo_exists():
            return

        self.clear_tools_frame()

        self.results = results

        for result in results:

            self.create_tool_card(
                result
            )

    # =====================================================
    # Create tool card
    # =====================================================

    def create_tool_card(self, result):
        """Create one tool management card."""

        card = BaseCard(
            self.tools_frame
        )

        card.configure(
            height=255
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

        installed_version = (
            result.version
            or "Not detected"
        )

        version_label = ctk.CTkLabel(
            card,
            text=(
                f"Version : "
                f"{installed_version}"
            ),
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        version_label.pack(
            anchor="w",
            padx=20
        )

        # -------------------------------------------------
        # Installation status
        # -------------------------------------------------

        if result.status == "Installed":

            status_color = (
                Theme.Colors.SUCCESS
            )

        elif result.status == "Incompatible":

            status_color = (
                Theme.Colors.WARNING
            )

        else:

            status_color = (
                Theme.Colors.ERROR
            )

        status_label = ctk.CTkLabel(
            card,
            text=(
                f"Status : "
                f"{result.status}"
            ),
            font=Theme.Fonts.BODY,
            text_color=status_color
        )

        status_label.pack(
            anchor="w",
            padx=20,
            pady=(8, 0)
        )

        # -------------------------------------------------
        # Path
        # -------------------------------------------------

        path_label = ctk.CTkLabel(
            card,
            text=(
                f"Path : "
                f"{result.path or 'Not available'}"
            ),
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        path_label.pack(
            anchor="w",
            padx=20,
            pady=(5, 0)
        )

        # -------------------------------------------------
        # Latest version
        # -------------------------------------------------

        latest = self.latest_versions.get(
            result.name
        )

        if latest:

            latest_label_text = (
                f"Latest : {latest}"
            )

        else:

            latest_label_text = (
                "Latest : Checking..."
            )

        latest_label = ctk.CTkLabel(
            card,
            text=latest_label_text,
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        latest_label.pack(
            anchor="w",
            padx=20,
            pady=(5, 0)
        )

        # -------------------------------------------------
        # Determine update state
        # -------------------------------------------------

        update_state = (
            self.get_update_state(
                result,
                latest
            )
        )

        # -------------------------------------------------
        # Update status label
        # -------------------------------------------------

        if result.status == "Missing":

            update_status_text = (
                "Update Status : Not Installed"
            )

            update_status_color = (
                Theme.Colors.SUBTEXT
            )

        elif update_state == "available":

            update_status_text = (
                "Update Status : Update Available"
            )

            update_status_color = (
                Theme.Colors.WARNING
            )

        elif update_state == "uptodate":

            update_status_text = (
                "Update Status : Up to Date"
            )

            update_status_color = (
                Theme.Colors.SUCCESS
            )

        else:

            update_status_text = (
                "Update Status : Checking..."
            )

            update_status_color = (
                Theme.Colors.SUBTEXT
            )

        update_status = ctk.CTkLabel(
            card,
            text=update_status_text,
            font=Theme.Fonts.BODY,
            text_color=update_status_color
        )

        update_status.pack(
            anchor="w",
            padx=20,
            pady=(5, 0)
        )

        # -------------------------------------------------
        # Buttons
        # -------------------------------------------------

        button_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=(8, 15)
        )

        # -------------------------------------------------
        # Missing tool
        # -------------------------------------------------

        if result.status == "Missing":

            install_button = ctk.CTkButton(
                button_frame,
                text="Install",
                width=110,
                height=34,
                command=lambda name=result.name:
                    self.install_tool(name)
            )

            install_button.pack(
                side="right"
            )

            return

        # -------------------------------------------------
        # Update available
        # -------------------------------------------------

        if update_state == "available":

            update_button = ctk.CTkButton(
                button_frame,
                text="Update",
                width=110,
                height=34,
                command=lambda name=result.name:
                    self.update_tool(name)
            )

            update_button.pack(
                side="right"
            )

    # =====================================================
    # Update state
    # =====================================================

    def get_update_state(
        self,
        result,
        latest
    ):
        """
        Determine whether a tool is up to date.

        Returns:
            "available"
            "uptodate"
            "checking"
        """

        if result.status == "Missing":
            return "checking"

        if not latest:
            return "checking"

        installed = result.version

        if not installed:
            return "checking"

        try:

            installed_parts = tuple(
                int(part)
                for part in str(
                    installed
                ).split(".")
            )

            latest_parts = tuple(
                int(part)
                for part in str(
                    latest
                ).split(".")
            )

            if latest_parts > installed_parts:

                return "available"

            return "uptodate"

        except ValueError:

            return "checking"

    # =====================================================
    # Installation
    # =====================================================

    def install_tool(self, tool_name):
        """Start automatic installation."""

        if (
            self.installing
            or self.updating
            or self.scanning
        ):
            return

        self.installing = True

        self.rescan_button.configure(
            state="disabled"
        )

        self.log_action(
            f"Installation requested for "
            f"{tool_name}."
        )

        self.show_operation_status(
            tool_name,
            "Starting automatic installation..."
        )

        thread = threading.Thread(
            target=self._perform_install,
            args=(tool_name,),
            daemon=True
        )

        thread.start()

    def _perform_install(self, tool_name):
        """Perform installation in background."""

        try:

            self.after(
                0,
                lambda: self.show_operation_status(
                    tool_name,
                    "Installing automatically..."
                )
            )

            if tool_name == "Git":

                success, path, message = (
                    ToolInstaller.install_git()
                )

            elif tool_name == "Python":

                success, path, message = (
                    ToolInstaller.install_python()
                )

            elif tool_name == "KiCad":

                success, path, message = (
                    ToolInstaller.install_kicad()
                )

            elif tool_name == "Ngspice":

                self.after(
                    0,
                    lambda: self.show_operation_status(
                        "Ngspice",
                        "Downloading and installing "
                        "the latest official release..."
                    )
                )

                success, path, message = (
                    ToolInstaller.install_ngspice()
                )

            else:

                success = False
                path = None
                message = (
                    f"Unsupported tool: "
                    f"{tool_name}"
                )

            if not success:

                self.log_action(
                    f"ERROR: {tool_name} "
                    f"installation failed. "
                    f"{message}"
                )

                raise RuntimeError(
                    message
                )

            self.log_action(
                f"{tool_name} installation completed. "
                f"{message}"
            )

            self.after(
                0,
                lambda name=tool_name,
                msg=message:
                    self.show_operation_status(
                        name,
                        msg
                        + "\n\nRescanning tools..."
                    )
            )

            self.after(
                1200,
                self.rescan
            )

        except Exception as error:

            error_message = str(
                error
            )

            self.log_action(
                f"ERROR: {tool_name} "
                f"installation failed: "
                f"{error_message}"
            )

            self.after(
                0,
                lambda message=error_message:
                    self.show_operation_error(
                        message
                    )
            )

        finally:

            self.after(
                0,
                self._finish_operation
            )

    # =====================================================
    # Update
    # =====================================================

    def update_tool(self, tool_name):
        """Start automatic update."""

        if (
            self.installing
            or self.updating
            or self.scanning
        ):
            return

        self.updating = True

        self.rescan_button.configure(
            state="disabled"
        )

        self.log_action(
            f"Update requested for "
            f"{tool_name}."
        )

        self.show_operation_status(
            tool_name,
            "Starting automatic update..."
        )

        thread = threading.Thread(
            target=self._perform_update,
            args=(tool_name,),
            daemon=True
        )

        thread.start()

    def _perform_update(self, tool_name):
        """Perform automatic update in background."""

        try:

            self.after(
                0,
                lambda: self.show_operation_status(
                    tool_name,
                    "Checking for available update..."
                )
            )

            if tool_name == "Git":

                success, path, message = (
                    ToolInstaller.update_git()
                )

            elif tool_name == "Python":

                success, path, message = (
                    ToolInstaller.update_python()
                )

            elif tool_name == "KiCad":

                success, path, message = (
                    ToolInstaller.update_kicad()
                )

            elif tool_name == "Ngspice":

                self.after(
                    0,
                    lambda: self.show_operation_status(
                        "Ngspice",
                        "Downloading and installing "
                        "the latest official release..."
                    )
                )

                success, path, message = (
                    ToolInstaller.update_ngspice()
                )

            else:

                success = False
                path = None
                message = (
                    f"Unsupported tool: "
                    f"{tool_name}"
                )

            if not success:

                self.log_action(
                    f"ERROR: {tool_name} "
                    f"update failed. "
                    f"{message}"
                )

                raise RuntimeError(
                    message
                )

            self.log_action(
                f"{tool_name} update completed. "
                f"{message}"
            )

            self.after(
                0,
                lambda name=tool_name,
                msg=message:
                    self.show_operation_status(
                        name,
                        msg
                        + "\n\nRescanning tools..."
                    )
            )

            self.after(
                1200,
                self.rescan
            )

        except Exception as error:

            error_message = str(
                error
            )

            self.log_action(
                f"ERROR: {tool_name} "
                f"update failed: "
                f"{error_message}"
            )

            self.after(
                0,
                lambda message=error_message:
                    self.show_operation_error(
                        message
                    )
            )

        finally:

            self.after(
                0,
                self._finish_operation
            )

    # =====================================================
    # Managed Python version
    # =====================================================

    @staticmethod
    def get_managed_python_latest_version():
        """
        Get the latest available version for the Python
        release line managed by ToolInstaller.

        Python is checked against the same WinGet package
        used for installation/update:
            Python.Python.3.12
        """

        if not ToolInstaller.get_winget_command():

            return None

        package_id = (
            ToolInstaller.WINGET_PACKAGES.get(
                "Python"
            )
        )

        if not package_id:

            return None

        # -------------------------------------------------
        # `winget show` does NOT support
        # --accept-package-agreements.
        #
        # Therefore explicitly disable package-agreement
        # handling for this read-only command.
        # -------------------------------------------------

        success, output = (
            ToolInstaller.run_winget(
                [
                    "show",
                    "--id",
                    package_id,
                    "-e",
                ],
                accept_package_agreement=False
            )
        )

        if (
            not success
            or not output
        ):

            return None

        # -------------------------------------------------
        # Find:
        #
        # Version: 3.12.10
        # -------------------------------------------------

        match = re.search(
            r"^Version\s*:\s*"
            r"(\d+(?:\.\d+)*)\s*$",
            output,
            re.IGNORECASE | re.MULTILINE
        )

        if match:

            return match.group(1)

        return None

    # =====================================================
    # Latest version checking
    # =====================================================

    def check_latest_versions(self, results):
        """
        Check latest versions in a background thread.

        This only checks versions.
        It does not install or update anything.
        """

        thread = threading.Thread(
            target=self._perform_latest_version_check,
            args=(results,),
            daemon=True
        )

        thread.start()

    def _perform_latest_version_check(
        self,
        results
    ):
        """Retrieve latest versions."""

        latest_versions = {}

        for result in results:

            try:

                # -------------------------------------------------
                # Ngspice has its own official release checker.
                # -------------------------------------------------

                if result.name == "Ngspice":

                    latest = (
                        ToolInstaller
                        .get_latest_ngspice_version()
                    )

                # -------------------------------------------------
                # Python uses its managed WinGet package.
                # -------------------------------------------------

                elif result.name == "Python":

                    latest = (
                        self
                        .get_managed_python_latest_version()
                    )

                # -------------------------------------------------
                # Git / KiCad use the existing updater.
                # -------------------------------------------------

                else:

                    latest = (
                        UpdateChecker
                        .get_latest_version(
                            result.name
                        )
                    )

                latest_versions[
                    result.name
                ] = latest

            except Exception:

                latest_versions[
                    result.name
                ] = None

        self.after(
            0,
            lambda versions=latest_versions:
                self._display_latest_versions(
                    versions
                )
        )

    def _display_latest_versions(
        self,
        latest_versions
    ):
        """Refresh cards with latest versions."""

        if not self.winfo_exists():
            return

        self.latest_versions = (
            latest_versions
        )

        self.load_tools(
            self.results
        )

    # =====================================================
    # Operation status
    # =====================================================

    def show_operation_status(
        self,
        tool_name,
        message
    ):
        """Display installation/update status."""

        if not self.winfo_exists():
            return

        self.clear_tools_frame()

        status_label = ctk.CTkLabel(
            self.tools_frame,
            text=(
                f"{tool_name}\n\n"
                f"{message}"
            ),
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        status_label.pack(
            pady=40
        )

    def show_operation_error(
        self,
        message
    ):
        """Display an operation error."""

        if not self.winfo_exists():
            return

        self.clear_tools_frame()

        error_label = ctk.CTkLabel(
            self.tools_frame,
            text=(
                "Operation failed.\n\n"
                f"{message}"
            ),
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.ERROR
        )

        error_label.pack(
            pady=40
        )

    def _finish_operation(self):
        """Finish an installation/update operation."""

        if not self.winfo_exists():
            return

        self.installing = False
        self.updating = False

        if not self.scanning:

            self.rescan_button.configure(
                state="normal"
            )

    # =====================================================
    # Rescan
    # =====================================================

    def rescan(self):
        """Start an automatic dependency scan."""

        if (
            self.scanning
            or self.installing
            or self.updating
        ):
            return

        self.scanning = True

        self.rescan_button.configure(
            text="Scanning...",
            state="disabled"
        )

        self.log_action(
            "Starting automatic dependency scan."
        )

        self.show_scan_status()

        thread = threading.Thread(
            target=self._perform_rescan,
            daemon=True
        )

        thread.start()

    def show_scan_status(self):
        """Display scanning status."""

        if not self.winfo_exists():
            return

        self.clear_tools_frame()

        status_label = ctk.CTkLabel(
            self.tools_frame,
            text="Scanning installed tools...",
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        status_label.pack(
            pady=30
        )

    def _perform_rescan(self):
        """Perform dependency scan in background."""

        try:

            checker = DependencyChecker()

            results = (
                checker.check_all()
            )

            self.after(
                0,
                lambda results=results:
                    self._display_rescan_results(
                        results
                    )
            )

        except Exception as error:

            error_message = str(
                error
            )

            self.log_action(
                "ERROR: Dependency scan failed: "
                f"{error_message}"
            )

            self.after(
                0,
                lambda message=error_message:
                    self._display_rescan_error(
                        message
                    )
            )

    def _display_rescan_results(
        self,
        results
    ):
        """Display fresh dependency results."""

        if not self.winfo_exists():
            return

        self.results = results

        self.scanning = False

        self.rescan_button.configure(
            text="Rescan",
            state="normal"
        )

        for result in results:

            self.log_action(
                f"Scan: {result.name} - "
                f"{result.status} - "
                f"version "
                f"{result.version or 'Unknown'}"
            )

        self.load_tools(
            results
        )

        # -------------------------------------------------
        # Check latest versions automatically.
        # -------------------------------------------------

        self.check_latest_versions(
            results
        )

        if self.on_scan_complete:

            self.on_scan_complete(
                results
            )

    def _display_rescan_error(
        self,
        error_message
    ):
        """Display dependency scan error."""

        if not self.winfo_exists():
            return

        self.scanning = False

        self.rescan_button.configure(
            text="Rescan",
            state="normal"
        )

        self.clear_tools_frame()

        error_label = ctk.CTkLabel(
            self.tools_frame,
            text=(
                "Dependency scan failed.\n\n"
                f"{error_message}"
            ),
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.ERROR
        )

        error_label.pack(
            pady=30
        )

    # =====================================================
    # Helpers
    # =====================================================

    def clear_tools_frame(self):
        """Remove all tool widgets."""

        for widget in (
            self.tools_frame.winfo_children()
        ):

            widget.destroy()