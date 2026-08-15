"""
------------------------------------------------------------
File Name : tool_installer.py

Purpose:
Handles installation actions for external eSim tools.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import json
import os
import platform
import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
import webbrowser

from config.config_manager import ConfigManager


class ToolInstaller:
    """Handles installation actions for supported tools."""

    # -------------------------------------------------
    # Download pages
    # -------------------------------------------------

    DOWNLOAD_PAGES = {
        "Git": "https://git-scm.com/install/windows",
        "Ngspice": (
            "https://sourceforge.net/projects/"
            "ngspice/files/ng-spice-rework/"
        ),
        "KiCad": "https://www.kicad.org/download/",
    }

    # -------------------------------------------------
    # Git
    # -------------------------------------------------

    GIT_RELEASE_API = (
        "https://api.github.com/repos/"
        "git-for-windows/git/releases/latest"
    )

    # -------------------------------------------------
    # Ngspice
    # -------------------------------------------------

    NGSPICE_VERSION = "46"

    NGSPICE_DOWNLOAD_URL = (
        "https://sourceforge.net/projects/"
        "ngspice/files/ng-spice-rework/"
        "old-releases/46/"
        "ngspice-46_64.7z/download"
    )

    NGSPICE_ARCHIVE_NAME = "ngspice-46_64.7z"

    NGSPICE_INSTALL_DIRECTORY = (
        Path.home()
        / "Downloads"
        / "eSim-Companion"
        / "Ngspice"
    )

    # -------------------------------------------------
    # General settings
    # -------------------------------------------------

    DOWNLOAD_DIRECTORY = (
        Path.home()
        / "Downloads"
        / "eSim-Companion"
    )

    TIMEOUT = 15
    EXTRACTION_TIMEOUT = 120

    # -------------------------------------------------
    # Open official download page
    # -------------------------------------------------

    @classmethod
    def open_download_page(cls, tool_name):
        """Open the official download page for a tool."""

        url = cls.DOWNLOAD_PAGES.get(tool_name)

        if not url:
            return False

        try:
            webbrowser.open(url)
            return True

        except OSError:
            return False

    # =================================================
    # Git
    # =================================================

    @classmethod
    def get_latest_git_installer_url(cls):
        """Get the latest official Git x64 installer URL."""

        if platform.system() != "Windows":
            return None

        try:
            request = urllib.request.Request(
                cls.GIT_RELEASE_API,
                headers={
                    "User-Agent": "eSim-Companion"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=cls.TIMEOUT
            ) as response:

                data = json.loads(
                    response.read().decode("utf-8")
                )

            assets = data.get("assets", [])

            for asset in assets:

                name = asset.get(
                    "name",
                    ""
                )

                if (
                    name.startswith("Git-")
                    and name.endswith("-64-bit.exe")
                ):
                    return asset.get(
                        "browser_download_url"
                    )

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            OSError,
            json.JSONDecodeError
        ):
            return None

        return None

    @classmethod
    def download_git_installer(cls):
        """Download the latest official Git x64 installer."""

        url = cls.get_latest_git_installer_url()

        if not url:
            return None

        filename = url.rsplit(
            "/",
            1
        )[-1]

        return cls.download_file(
            url,
            filename
        )

    @classmethod
    def launch_installer(cls, installer_path):
        """Launch a downloaded Windows installer."""

        if not installer_path:
            return False

        path = Path(installer_path)

        if not path.is_file():
            return False

        if platform.system() != "Windows":
            return False

        try:
            os.startfile(
                str(path)
            )

            return True

        except OSError:
            return False

    # =================================================
    # Generic download
    # =================================================

    @classmethod
    def download_file(cls, url, filename):
        """Download a file to the eSim Companion directory."""

        if not url:
            return None

        try:
            cls.DOWNLOAD_DIRECTORY.mkdir(
                parents=True,
                exist_ok=True
            )

            destination = (
                cls.DOWNLOAD_DIRECTORY
                / filename
            )

            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "eSim-Companion"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=cls.TIMEOUT
            ) as response:

                with open(
                    destination,
                    "wb"
                ) as file:

                    while True:

                        chunk = response.read(
                            1024 * 1024
                        )

                        if not chunk:
                            break

                        file.write(chunk)

            if not destination.exists():
                return None

            if destination.stat().st_size == 0:

                destination.unlink(
                    missing_ok=True
                )

                return None

            return str(destination)

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            OSError
        ):
            return None

    # =================================================
    # Ngspice
    # =================================================

    @classmethod
    def get_ngspice_archive_path(cls):
        """Return the expected Ngspice archive path."""

        return (
            cls.DOWNLOAD_DIRECTORY
            / cls.NGSPICE_ARCHIVE_NAME
        )

    @classmethod
    def get_ngspice_executable(cls):
        """
        Return the Ngspice GUI executable path.

        This executable is used when actual Ngspice
        simulation needs to be launched.
        """

        executable = (
            cls.NGSPICE_INSTALL_DIRECTORY
            / "Spice64"
            / "bin"
            / "ngspice.exe"
        )

        if executable.is_file():
            return executable

        return None

    @classmethod
    def get_ngspice_console_executable(cls):
        """
        Return the Ngspice console executable path.

        ngspice_con.exe is used for version checking
        because ngspice.exe launches the GUI.
        """

        executable = (
            cls.NGSPICE_INSTALL_DIRECTORY
            / "Spice64"
            / "bin"
            / "ngspice_con.exe"
        )

        if executable.is_file():
            return executable

        return None

    @classmethod
    def download_ngspice(cls):
        """Download the official Ngspice Windows 64-bit package."""

        return cls.download_file(
            cls.NGSPICE_DOWNLOAD_URL,
            cls.NGSPICE_ARCHIVE_NAME
        )

    @classmethod
    def extract_ngspice(cls, archive_path):
        """Extract the Ngspice archive using Windows tar."""

        if platform.system() != "Windows":
            return None

        if not archive_path:
            return None

        archive = Path(archive_path)

        if not archive.is_file():
            return None

        # -------------------------------------------------
        # Find tar
        # -------------------------------------------------

        tar_command = shutil.which("tar")

        if not tar_command:

            system_tar = (
                Path(
                    os.environ.get(
                        "SystemRoot",
                        r"C:\Windows"
                    )
                )
                / "System32"
                / "tar.exe"
            )

            if system_tar.is_file():
                tar_command = str(system_tar)

        if not tar_command:
            return None

        try:

            cls.NGSPICE_INSTALL_DIRECTORY.mkdir(
                parents=True,
                exist_ok=True
            )

            result = subprocess.run(
                [
                    tar_command,
                    "-xf",
                    str(archive),
                    "-C",
                    str(
                        cls.NGSPICE_INSTALL_DIRECTORY
                    )
                ],
                capture_output=True,
                text=True,
                timeout=cls.EXTRACTION_TIMEOUT
            )

            if result.returncode != 0:
                return None

            # Check GUI executable
            gui_executable = (
                cls.get_ngspice_executable()
            )

            # Check console executable
            console_executable = (
                cls.get_ngspice_console_executable()
            )

            if not gui_executable:
                return None

            if not console_executable:
                return None

            # Return console executable because this is
            # the executable that should be used for
            # version detection.
            return str(console_executable)

        except (
            subprocess.SubprocessError,
            OSError
        ):
            return None

    @classmethod
    def verify_ngspice(cls, executable_path=None):
        """
        Verify Ngspice using the console executable.

        IMPORTANT:
        Do not execute ngspice.exe here because it opens
        the Ngspice GUI.

        ngspice_con.exe -v is used instead.
        """

        # -------------------------------------------------
        # Prefer the console executable automatically
        # -------------------------------------------------

        console_executable = (
            cls.get_ngspice_console_executable()
        )

        if console_executable:
            executable = Path(
                console_executable
            )

        else:

            if not executable_path:
                return False

            provided_path = Path(
                executable_path
            )

            # If the supplied path is ngspice.exe,
            # replace it with ngspice_con.exe.
            if (
                provided_path.name.lower()
                == "ngspice.exe"
            ):

                executable = (
                    provided_path.parent
                    / "ngspice_con.exe"
                )

            else:

                executable = provided_path

        if not executable.is_file():
            return False

        try:

            result = subprocess.run(
                [
                    str(executable),
                    "-v"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )

            output = (
                result.stdout
                or result.stderr
                or ""
            )

            # -------------------------------------------------
            # Verify successful execution
            # -------------------------------------------------

            if result.returncode != 0:
                return False

            # -------------------------------------------------
            # Confirm that the expected Ngspice version
            # is present in the output.
            # -------------------------------------------------

            return (
                "ngspice" in output.lower()
                and cls.NGSPICE_VERSION in output
            )

        except (
            subprocess.SubprocessError,
            OSError
        ):
            return False

    @classmethod
    def install_ngspice(cls):
        """
        Download, extract, verify, and configure Ngspice.

        The console executable is saved in ConfigManager
        so the dependency checker can perform version
        checks without opening the Ngspice GUI.
        """

        if platform.system() != "Windows":

            return (
                False,
                None,
                "Ngspice installation is supported "
                "on Windows only."
            )

        # =================================================
        # Check existing installation
        # =================================================

        existing_console = (
            cls.get_ngspice_console_executable()
        )

        if existing_console:

            if cls.verify_ngspice(
                existing_console
            ):

                ConfigManager.set_path(
                    "Ngspice",
                    str(existing_console)
                )

                return (
                    True,
                    str(existing_console),
                    "Ngspice is already installed."
                )

        # =================================================
        # Download
        # =================================================

        archive_path = cls.download_ngspice()

        if not archive_path:

            return (
                False,
                None,
                "Unable to download Ngspice."
            )

        # =================================================
        # Extract
        # =================================================

        console_executable = (
            cls.extract_ngspice(
                archive_path
            )
        )

        if not console_executable:

            return (
                False,
                None,
                "Unable to extract the Ngspice package."
            )

        # =================================================
        # Verify
        # =================================================

        if not cls.verify_ngspice(
            console_executable
        ):

            return (
                False,
                None,
                "Ngspice was extracted but could "
                "not be verified."
            )

        # =================================================
        # Save configuration
        # =================================================

        ConfigManager.set_path(
            "Ngspice",
            console_executable
        )

        # =================================================
        # Return success
        # =================================================

        return (
            True,
            console_executable,
            "Ngspice installed successfully."
        )