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

import threading

import customtkinter as ctk

from utils.theme import Theme
from services.dependency_checker import DependencyChecker
from gui.components.base_card import BaseCard
from services.tool_installer import ToolInstaller


class ToolsLayout(ctk.CTkFrame):
    """Tools management page."""

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

        self.create_layout()

    # =================================================
    # Layout
    # =================================================

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

    # =================================================
    # Load Tools
    # =================================================

    def load_tools(self):
        """Check and display all configured tools."""

        self.clear_tools_frame()

        checker = DependencyChecker()

        results = checker.check_all()

        for result in results:
            self.create_tool_card(result)

    # =================================================
    # Tool Card
    # =================================================

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

        elif result.status == "Incompatible":

            action_button = ctk.CTkButton(
                card,
                text="Update",
                width=110,
                height=34,
                command=lambda name=result.name:
                    self.install_tool(name)
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

    # =================================================
    # Installation
    # =================================================

    def install_tool(self, tool_name):
        """Start installation of a supported tool."""

        if self.installing or self.scanning:
            return

        self.installing = True

        self.rescan_button.configure(
            text="Installing...",
            state="disabled"
        )

        self.show_install_status(
            tool_name,
            "Preparing installation..."
        )

        thread = threading.Thread(
            target=self._perform_install,
            args=(tool_name,),
            daemon=True
        )

        thread.start()

    def _perform_install(self, tool_name):
        """Perform installation in a background thread."""

        try:

            # =================================================
            # Git
            # =================================================

            if tool_name == "Git":

                self.after(
                    0,
                    lambda: self.show_install_status(
                        "Git",
                        "Finding latest Git installer..."
                    )
                )

                installer_url = (
                    ToolInstaller.get_latest_git_installer_url()
                )

                if not installer_url:

                    raise RuntimeError(
                        "Unable to find the latest "
                        "Git installer."
                    )

                self.after(
                    0,
                    lambda: self.show_install_status(
                        "Git",
                        "Downloading Git installer..."
                    )
                )

                filename = installer_url.rsplit(
                    "/",
                    1
                )[-1]

                installer_path = (
                    ToolInstaller.download_file(
                        installer_url,
                        filename
                    )
                )

                if not installer_path:

                    raise RuntimeError(
                        "Git installer download failed."
                    )

                self.after(
                    0,
                    lambda: self.show_install_status(
                        "Git",
                        "Launching Git installer..."
                    )
                )

                launched = (
                    ToolInstaller.launch_installer(
                        installer_path
                    )
                )

                if not launched:

                    raise RuntimeError(
                        "Unable to launch the "
                        "Git installer."
                    )

                self.after(
                    0,
                    lambda: self.show_install_status(
                        "Git",
                        "Git installer launched.\n\n"
                        "Complete the installation, "
                        "then click Rescan."
                    )
                )

            # =================================================
            # Ngspice
            # =================================================

            elif tool_name == "Ngspice":

                self.after(
                    0,
                    lambda: self.show_install_status(
                        "Ngspice",
                        "Checking Ngspice installation..."
                    )
                )

                success, executable_path, message = (
                    ToolInstaller.install_ngspice()
                )

                if not success:

                    raise RuntimeError(
                        message
                    )

                self.after(
                    0,
                    lambda message=message:
                        self.show_install_status(
                            "Ngspice",
                            message
                        )
                )

                self.after(
                    1000,
                    self._rescan_after_install
                )

                return

            # =================================================
            # Other tools
            # =================================================

            else:

                success = (
                    ToolInstaller.open_download_page(
                        tool_name
                    )
                )

                if not success:

                    raise RuntimeError(
                        f"No download page available "
                        f"for {tool_name}."
                    )

                self.after(
                    0,
                    lambda name=tool_name:
                        self.show_install_status(
                            name,
                            "Official download page opened.\n\n"
                            "Complete the installation, "
                            "then click Rescan."
                        )
                )

        except Exception as error:

            error_message = str(error)

            self.after(
                0,
                lambda message=error_message:
                    self.show_install_error(
                        message
                    )
            )

        finally:

            # Ngspice performs its own delayed rescan.
            if tool_name != "Ngspice":

                self.after(
                    0,
                    self._finish_install
                )

    # =================================================
    # Installation UI
    # =================================================

    def show_install_status(
        self,
        tool_name,
        message
    ):
        """Display installation status."""

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
            pady=30
        )

    def show_install_error(self, message):
        """Display an installation error."""

        if not self.winfo_exists():
            return

        self.clear_tools_frame()

        error_label = ctk.CTkLabel(
            self.tools_frame,
            text=(
                "Installation failed.\n\n"
                f"{message}"
            ),
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.ERROR
        )

        error_label.pack(
            pady=30
        )

        self.installing = False

        self.rescan_button.configure(
            text="Rescan",
            state="normal"
        )

    def clear_tools_frame(self):
        """Remove all widgets from the tools container."""

        for widget in self.tools_frame.winfo_children():
            widget.destroy()

    def _finish_install(self):
        """Finish a normal installation operation."""

        if not self.winfo_exists():
            return

        if self.scanning:
            return

        self.installing = False

        self.rescan_button.configure(
            text="Rescan",
            state="normal"
        )

    def _rescan_after_install(self):
        """Rescan tools after successful Ngspice installation."""

        if not self.winfo_exists():
            return

        self.installing = False

        self.rescan()

    # =================================================
    # Rescan
    # =================================================

    def rescan(self):
        """Start a background dependency scan."""

        if self.scanning or self.installing:
            return

        self.scanning = True

        self.rescan_button.configure(
            text="Scanning...",
            state="disabled"
        )

        self.show_scan_status()

        thread = threading.Thread(
            target=self._perform_rescan,
            daemon=True
        )

        thread.start()

    def show_scan_status(self):
        """Display the scanning status."""

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
        """Perform the dependency scan in the background."""

        try:

            checker = DependencyChecker()

            results = checker.check_all()

            self.after(
                0,
                lambda results=results:
                    self._display_rescan_results(
                        results
                    )
            )

        except Exception as error:

            error_message = str(error)

            self.after(
                0,
                lambda message=error_message:
                    self._display_rescan_error(
                        message
                    )
            )

    def _display_rescan_results(self, results):
        """Update the UI with fresh scan results."""

        if not self.winfo_exists():
            return

        self.clear_tools_frame()

        for result in results:
            self.create_tool_card(result)

        if self.on_scan_complete:
            self.on_scan_complete(results)

        self.scanning = False

        self.installing = False

        self.rescan_button.configure(
            text="Rescan",
            state="normal"
        )

    def _display_rescan_error(self, error_message):
        """Display a dependency scan error."""

        if not self.winfo_exists():
            return

        self.scanning = False

        self.installing = False

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