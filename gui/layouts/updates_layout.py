"""
------------------------------------------------------------
File Name : updates_layout.py

Purpose:
Displays update information for eSim Companion tools.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import queue
import threading
from concurrent.futures import ThreadPoolExecutor

import customtkinter as ctk

from utils.theme import Theme
from services.dependency_checker import DependencyChecker
from gui.components.base_card import BaseCard
from services.update_checker import UpdateChecker


class UpdatesLayout(ctk.CTkFrame):
    """Displays available update information."""

    def __init__(self, parent):
        super().__init__(
            master=parent,
            fg_color=Theme.Colors.BACKGROUND
        )

        self.checking = False
        self.result_queue = queue.Queue()
        self.poll_job = None

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

        # -------------------------------------------------
        # Initial loading
        # -------------------------------------------------

        self.show_loading_message()
        self.start_update_check()

    def show_loading_message(self):
        """Display a loading message."""

        for widget in self.updates_frame.winfo_children():
            widget.destroy()

        loading_label = ctk.CTkLabel(
            self.updates_frame,
            text="Checking dependencies and updates...",
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        loading_label.pack(
            pady=30
        )

    def start_update_check(self):
        """Start update checking in a background thread."""

        if self.checking:
            return

        self.checking = True

        self.check_button.configure(
            text="Checking...",
            state="disabled"
        )

        worker = threading.Thread(
            target=self._perform_update_check,
            daemon=True
        )

        worker.start()

        self.poll_job = self.after(
            100,
            self._poll_results
        )

    def _perform_update_check(self):
        """Perform dependency and update checks in background."""

        try:

            # -------------------------------------------------
            # Dependency scan
            # -------------------------------------------------

            checker = DependencyChecker()

            results = checker.check_all()

            # -------------------------------------------------
            # Parallel latest-version checks
            # -------------------------------------------------

            update_results = []

            with ThreadPoolExecutor(
                max_workers=4
            ) as executor:

                futures = [
                    executor.submit(
                        UpdateChecker.get_latest_version,
                        result.name
                    )
                    for result in results
                ]

                for result, future in zip(
                    results,
                    futures
                ):

                    try:
                        latest_version = future.result()

                    except Exception:
                        latest_version = None

                    update_results.append(
                        (
                            result,
                            latest_version
                        )
                    )

            # -------------------------------------------------
            # Store successful result
            # -------------------------------------------------

            self.result_queue.put(
                (
                    "success",
                    update_results
                )
            )

        except Exception as error:

            self.result_queue.put(
                (
                    "error",
                    str(error)
                )
            )

    def _poll_results(self):
        """Check for background results on the UI thread."""

        try:

            result_type, data = (
                self.result_queue.get_nowait()
            )

        except queue.Empty:

            if self.winfo_exists():

                self.poll_job = self.after(
                    100,
                    self._poll_results
                )

            return

        self.poll_job = None

        if not self.winfo_exists():
            return

        if result_type == "success":

            self._display_results(data)

        else:

            self._show_error(data)

    def _display_results(self, update_results):
        """Display update results on the UI thread."""

        if not self.winfo_exists():
            return

        for widget in self.updates_frame.winfo_children():
            widget.destroy()

        for result, latest_version in update_results:

            self.create_update_card(
                result,
                latest_version
            )

        self.checking = False

        self.check_button.configure(
            text="Check for Updates",
            state="normal"
        )

    def _show_error(self, error_message):
        """Display an error if update checking fails."""

        if not self.winfo_exists():
            return

        for widget in self.updates_frame.winfo_children():
            widget.destroy()

        error_label = ctk.CTkLabel(
            self.updates_frame,
            text=(
                "Unable to complete update check.\n\n"
                f"{error_message}"
            ),
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.ERROR
        )

        error_label.pack(
            pady=30
        )

        self.checking = False

        self.check_button.configure(
            text="Check for Updates",
            state="normal"
        )

    def create_update_card(
        self,
        result,
        latest_version
    ):
        """Create an update card for a tool."""

        card = BaseCard(
            self.updates_frame
        )

        card.pack(
            fill="x",
            padx=5,
            pady=8,
            ipady=8
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

            status_text = UpdateChecker.compare_versions(
                result.version,
                latest_version
            )

            if status_text == "Update Available":

                status_color = Theme.Colors.WARNING

            elif status_text == "Up to Date":

                status_color = Theme.Colors.SUCCESS

            elif status_text == "Newer Than Latest":

                status_color = Theme.Colors.WARNING

            else:

                status_color = Theme.Colors.SUBTEXT

        # -------------------------------------------------
        # Latest version
        # -------------------------------------------------

        latest_text = (
            latest_version
            if latest_version
            else "Unavailable"
        )

        latest_label = ctk.CTkLabel(
            card,
            text=f"Latest Version : {latest_text}",
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT
        )

        latest_label.pack(
            anchor="w",
            padx=20,
            pady=(5, 0)
        )

        # -------------------------------------------------
        # Update status
        # -------------------------------------------------

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

        if self.checking:
            return

        self.show_loading_message()
        self.start_update_check()

    def destroy(self):
        """Clean up scheduled UI polling before destruction."""

        if self.poll_job is not None:

            try:
                self.after_cancel(
                    self.poll_job
                )

            except Exception:
                pass

            self.poll_job = None

        super().destroy()