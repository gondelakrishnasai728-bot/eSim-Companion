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
import re
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
        "Git": (
            "https://git-scm.com/install/windows"
        ),

        "Ngspice": (
            "https://sourceforge.net/projects/"
            "ngspice/files/ng-spice-rework/"
        ),

        "KiCad": (
            "https://www.kicad.org/download/windows/"
        ),
    }

    # =================================================
    # Git
    # =================================================

    GIT_RELEASE_API = (
        "https://api.github.com/repos/"
        "git-for-windows/git/releases/latest"
    )

    # =================================================
    # KiCad
    # =================================================

    KICAD_DOWNLOAD_PAGE = (
        "https://www.kicad.org/download/windows/"
    )

    KICAD_INSTALLER_PATTERN = re.compile(
        r'href=["\']([^"\']*'
        r'kicad[^"\']*'
        r'(?:x86_64|x64|64)[^"\']*'
        r'\.exe(?:\?[^"\']*)?)["\']',
        re.IGNORECASE
    )

    KICAD_INSTALL_DIRECTORY = Path(
        "C:/Program Files/KiCad"
    )

    # =================================================
    # Ngspice
    # =================================================

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

    # =================================================
    # General settings
    # =================================================

    DOWNLOAD_DIRECTORY = (
        Path.home()
        / "Downloads"
        / "eSim-Companion"
    )

    TIMEOUT = 60
    EXTRACTION_TIMEOUT = 120

    # =================================================
    # Open official download page
    # =================================================

    @classmethod
    def open_download_page(cls, tool_name):
        """Open the official download page for a tool."""

        url = cls.DOWNLOAD_PAGES.get(
            tool_name
        )

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
                    response.read().decode(
                        "utf-8"
                    )
                )

            assets = data.get(
                "assets",
                []
            )

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

        path = Path(
            installer_path
        )

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
        """
        Download a file to the eSim Companion directory.

        Uses Windows curl.exe when available because it
        provides visible download progress and handles
        large files more reliably.

        Falls back to urllib if curl is unavailable.
        """

        if not url:
            return None

        destination = (
            cls.DOWNLOAD_DIRECTORY
            / filename
        )

        try:

            cls.DOWNLOAD_DIRECTORY.mkdir(
                parents=True,
                exist_ok=True
            )

            # -------------------------------------------------
            # Remove incomplete previous download.
            # -------------------------------------------------

            if destination.exists():

                try:
                    destination.unlink()

                except OSError:
                    return None

            # -------------------------------------------------
            # Prefer curl on Windows.
            # -------------------------------------------------

            curl_command = shutil.which(
                "curl.exe"
            )

            if curl_command:

                print(
                    f"\nDownloading: {filename}"
                )

                print(
                    f"Source: {url}"
                )

                result = subprocess.run(
                    [
                        curl_command,
                        "-L",
                        "--fail",
                        "--retry",
                        "3",
                        "--retry-delay",
                        "2",
                        "--connect-timeout",
                        "30",
                        "--output",
                        str(destination),
                        url,
                    ],
                    timeout=None
                )

                if result.returncode != 0:

                    if destination.exists():

                        try:
                            destination.unlink()

                        except OSError:
                            pass

                    return None

            else:

                # -------------------------------------------------
                # urllib fallback
                # -------------------------------------------------

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

                    total_size = response.headers.get(
                        "Content-Length"
                    )

                    try:

                        total_size = (
                            int(total_size)
                            if total_size
                            else None
                        )

                    except ValueError:

                        total_size = None

                    downloaded = 0

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

                            file.write(
                                chunk
                            )

                            downloaded += len(
                                chunk
                            )

                            if total_size:

                                percentage = (
                                    downloaded
                                    * 100
                                    / total_size
                                )

                                print(
                                    f"\rDownloading "
                                    f"{percentage:6.2f}%",
                                    end="",
                                    flush=True
                                )

                            else:

                                size_mb = (
                                    downloaded
                                    / (
                                        1024 * 1024
                                    )
                                )

                                print(
                                    f"\rDownloaded "
                                    f"{size_mb:.1f} MB",
                                    end="",
                                    flush=True
                                )

                    print()

            # -------------------------------------------------
            # Validate destination.
            # -------------------------------------------------

            if not destination.exists():
                return None

            if destination.stat().st_size == 0:

                destination.unlink(
                    missing_ok=True
                )

                return None

            print(
                f"Download completed: "
                f"{destination}"
            )

            return str(
                destination
            )

        except KeyboardInterrupt:

            print(
                "\nDownload cancelled."
            )

            try:
                destination.unlink(
                    missing_ok=True
                )

            except OSError:
                pass

            return None

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            OSError,
            subprocess.SubprocessError
        ):

            try:

                destination.unlink(
                    missing_ok=True
                )

            except OSError:
                pass

            return None

    # =================================================
    # KiCad
    # =================================================

    @classmethod
    def get_kicad_download_page(cls):
        """Return the official KiCad Windows download page."""

        return cls.KICAD_DOWNLOAD_PAGE

    @classmethod
    def get_latest_kicad_installer_url(cls):
        """
        Find the current official KiCad Windows x86-64
        installer URL from the official download page.
        """

        if platform.system() != "Windows":
            return None

        try:

            request = urllib.request.Request(
                cls.KICAD_DOWNLOAD_PAGE,
                headers={
                    "User-Agent": "eSim-Companion"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=cls.TIMEOUT
            ) as response:

                html = response.read().decode(
                    "utf-8",
                    errors="ignore"
                )

            matches = (
                cls.KICAD_INSTALLER_PATTERN.findall(
                    html
                )
            )

            if not matches:
                return None

            for url in matches:

                url = url.replace(
                    "&amp;",
                    "&"
                )

                if url.startswith("//"):

                    url = (
                        "https:"
                        + url
                    )

                elif url.startswith("/"):

                    url = (
                        "https://www.kicad.org"
                        + url
                    )

                elif not (
                    url.startswith("http://")
                    or url.startswith("https://")
                ):

                    continue

                return url

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            OSError
        ):

            return None

        return None

    @classmethod
    def get_kicad_installed_executable(cls):
        """
        Find the installed KiCad executable.

        Typical location:

        C:\\Program Files\\KiCad\\10.0\\bin\\kicad.exe
        """

        if platform.system() != "Windows":
            return None

        program_files = [
            os.environ.get(
                "ProgramFiles"
            ),
            os.environ.get(
                "ProgramW6432"
            ),
        ]

        possible_roots = []

        for root in program_files:

            if root:

                possible_roots.append(
                    Path(root)
                    / "KiCad"
                )

        possible_roots.append(
            Path(
                "C:/Program Files/KiCad"
            )
        )

        for root in possible_roots:

            if not root.is_dir():
                continue

            try:

                executables = list(
                    root.glob(
                        "*/bin/kicad.exe"
                    )
                )

            except OSError:

                continue

            if executables:

                executables.sort(
                    reverse=True
                )

                return executables[0]

        return None

    @classmethod
    def get_existing_kicad_installer(
        cls,
        filename=None
    ):
        """
        Return an existing KiCad installer from the
        eSim Companion download directory.

        If filename is provided, only that exact installer
        is checked.
        """

        if filename:

            installer = (
                cls.DOWNLOAD_DIRECTORY
                / filename
            )

            if installer.is_file():

                try:

                    if installer.stat().st_size > 0:
                        return installer

                except OSError:
                    return None

            return None

        # -------------------------------------------------
        # Fallback: search for KiCad Windows installers.
        # -------------------------------------------------

        try:

            installers = list(
                cls.DOWNLOAD_DIRECTORY.glob(
                    "kicad-*.exe"
                )
            )

        except OSError:

            return None

        valid_installers = []

        for installer in installers:

            try:

                if (
                    installer.is_file()
                    and installer.stat().st_size > 0
                ):

                    valid_installers.append(
                        installer
                    )

            except OSError:
                continue

        if not valid_installers:
            return None

        valid_installers.sort(
            key=lambda path: path.stat().st_mtime,
            reverse=True
        )

        return valid_installers[0]

    @classmethod
    def install_kicad(cls):
        """
        Download and launch the official KiCad
        Windows x86-64 installer.

        If the installer has already been downloaded,
        reuse the existing installer instead of
        downloading the large file again.
        """

        if platform.system() != "Windows":

            return (
                False,
                None,
                "KiCad installation is supported "
                "on Windows only."
            )

        # =================================================
        # Check existing installation
        # =================================================

        existing_executable = (
            cls.get_kicad_installed_executable()
        )

        if existing_executable:

            ConfigManager.set_path(
                "KiCad",
                str(
                    existing_executable
                )
            )

            return (
                True,
                str(
                    existing_executable
                ),
                "KiCad is already installed."
            )

        # =================================================
        # Find latest installer
        # =================================================

        installer_url = (
            cls.get_latest_kicad_installer_url()
        )

        if not installer_url:

            return (
                False,
                None,
                "Unable to find the official "
                "KiCad Windows x64 installer."
            )

        # =================================================
        # Determine filename
        # =================================================

        filename = (
            installer_url
            .split(
                "?",
                1
            )[0]
            .rsplit(
                "/",
                1
            )[-1]
        )

        if not filename.lower().endswith(
            ".exe"
        ):

            filename = (
                "kicad-windows-installer.exe"
            )

        # =================================================
        # Check for existing downloaded installer
        # =================================================

        existing_installer = (
            cls.get_existing_kicad_installer(
                filename
            )
        )

        if existing_installer:

            installer_path = str(
                existing_installer
            )

            print(
                f"Using existing KiCad installer: "
                f"{installer_path}"
            )

        else:

            # =================================================
            # Download installer
            # =================================================

            print(
                "KiCad installer not found locally."
            )

            print(
                "Starting KiCad installer download..."
            )

            installer_path = (
                cls.download_file(
                    installer_url,
                    filename
                )
            )

            if not installer_path:

                return (
                    False,
                    None,
                    "Unable to download the "
                    "KiCad installer."
                )

        # =================================================
        # Launch installer
        # =================================================

        launched = (
            cls.launch_installer(
                installer_path
            )
        )

        if not launched:

            return (
                False,
                installer_path,
                "KiCad installer is available "
                "but could not be launched."
            )

        # =================================================
        # Return success
        # =================================================

        return (
            True,
            installer_path,
            "KiCad installer launched successfully. "
            "Complete the installation, then click "
            "Rescan."
        )

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

        archive = Path(
            archive_path
        )

        if not archive.is_file():
            return None

        # -------------------------------------------------
        # Find tar
        # -------------------------------------------------

        tar_command = shutil.which(
            "tar"
        )

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

                tar_command = str(
                    system_tar
                )

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

            gui_executable = (
                cls.get_ngspice_executable()
            )

            console_executable = (
                cls.get_ngspice_console_executable()
            )

            if not gui_executable:
                return None

            if not console_executable:
                return None

            return str(
                console_executable
            )

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

            if result.returncode != 0:
                return False

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
                    str(
                        existing_console
                    )
                )

                return (
                    True,
                    str(
                        existing_console
                    ),
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
                "Unable to extract the "
                "Ngspice package."
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

        return (
            True,
            console_executable,
            "Ngspice installed successfully."
        )