"""
------------------------------------------------------------
File Name : tool_installer.py

Purpose:
Handles installation and update actions for external
eSim tools.

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
import time
import urllib.error
import urllib.request
from pathlib import Path
import webbrowser

from config.config_manager import ConfigManager


class ToolInstaller:
    """Handles installation and update actions for supported tools."""

    # =================================================
    # Official download pages
    # =================================================

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
    # WinGet
    # =================================================

    WINGET_TIMEOUT = 900

    WINGET_PACKAGES = {
        "Git": "Git.Git",
        "Python": "Python.Python.3.12",
        "KiCad": "KiCad.KiCad",
    }

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

    # Retained for compatibility with existing code.
    #
    # Installation and update operations do NOT rely
    # on this value. The official SourceForge page is
    # checked dynamically.
    NGSPICE_VERSION = "46"

    NGSPICE_DOWNLOAD_URL = (
        "https://sourceforge.net/projects/"
        "ngspice/files/ng-spice-rework/"
        "46/"
        "ngspice-46_64.7z/download"
    )

    NGSPICE_ARCHIVE_NAME = (
        "ngspice-46_64.7z"
    )

    NGSPICE_INSTALL_DIRECTORY = (
        Path.home()
        / "Downloads"
        / "eSim-Companion"
        / "Ngspice"
    )

    # Number of times SourceForge is queried when
    # determining the latest Ngspice release.
    NGSPICE_VERSION_CHECK_RETRIES = 3

    # Delay between failed SourceForge requests.
    NGSPICE_RETRY_DELAY = 2

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
    # WinGet
    # =================================================

    @classmethod
    def get_winget_command(cls):
        """
        Return the WinGet executable path.

        WinGet is used for automated installation and
        updating of supported Windows tools.
        """

        if platform.system() != "Windows":
            return None

        return shutil.which(
            "winget.exe"
        )

    @classmethod
    def run_winget(
        cls,
        arguments,
        accept_package_agreement=True
    ):
        """
        Execute a WinGet command.

        Source agreements are automatically accepted.

        Package agreements are accepted by default for
        install and upgrade operations.

        Some WinGet commands, such as `show`, do not
        support --accept-package-agreements. Therefore
        callers can disable that option by passing:

            accept_package_agreement=False

        Returns:
            tuple:
                success: bool
                output: str
        """

        winget = cls.get_winget_command()

        if not winget:

            return (
                False,
                "WinGet is not available on this system."
            )

        # -------------------------------------------------
        # Base WinGet command
        # -------------------------------------------------

        command = [
            winget,
            *arguments,
            "--source",
            "winget",
            "--accept-source-agreements",
        ]

        # -------------------------------------------------
        # Package agreements are required for operations
        # such as install and upgrade, but NOT for `show`.
        # -------------------------------------------------

        if accept_package_agreement:

            command.append(
                "--accept-package-agreements"
            )

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=cls.WINGET_TIMEOUT,
                stdin=subprocess.DEVNULL,
                creationflags=(
                    subprocess.CREATE_NO_WINDOW
                    if os.name == "nt"
                    else 0
                )
            )

            output_parts = []

            if result.stdout:

                output_parts.append(
                    result.stdout.strip()
                )

            if result.stderr:

                output_parts.append(
                    result.stderr.strip()
                )

            output = "\n".join(
                part
                for part in output_parts
                if part
            )

            return (
                result.returncode == 0,
                output
            )

        except subprocess.TimeoutExpired:

            return (
                False,
                "WinGet operation timed out."
            )

        except (
            subprocess.SubprocessError,
            OSError
        ) as exc:

            return (
                False,
                str(exc)
            )

    @classmethod
    def winget_install(cls, package_id):
        """Install a package automatically using WinGet."""

        return cls.run_winget(
            [
                "install",
                "--id",
                package_id,
                "-e",
                "--silent",
            ]
        )

    @classmethod
    def winget_upgrade(cls, package_id):
        """Upgrade a package automatically using WinGet."""

        return cls.run_winget(
            [
                "upgrade",
                "--id",
                package_id,
                "-e",
                "--silent",
            ]
        )

    @classmethod
    def install_with_winget(cls, tool_name):
        """Automatically install a supported tool using WinGet."""

        package_id = cls.WINGET_PACKAGES.get(
            tool_name
        )

        if not package_id:

            return (
                False,
                None,
                f"No WinGet package is configured "
                f"for {tool_name}."
            )

        success, output = cls.winget_install(
            package_id
        )

        if not success:

            return (
                False,
                None,
                f"Unable to install {tool_name} "
                f"automatically using WinGet.\n"
                f"{output}"
            )

        return (
            True,
            package_id,
            f"{tool_name} installed successfully "
            f"using WinGet."
        )

    @classmethod
    def update_with_winget(cls, tool_name):
        """
        Automatically update a supported tool using WinGet.

        If no newer version is available, the operation is
        considered successful because the tool is already
        up to date.
        """

        package_id = cls.WINGET_PACKAGES.get(
            tool_name
        )

        if not package_id:

            return (
                False,
                None,
                f"No WinGet package is configured "
                f"for {tool_name}."
            )

        success, output = cls.winget_upgrade(
            package_id
        )

        if success:

            return (
                True,
                package_id,
                f"{tool_name} updated successfully "
                f"using WinGet."
            )

        normalized_output = (
            output.lower()
        )

        if (
            "no available upgrade found"
            in normalized_output
            or
            "no newer package versions"
            in normalized_output
        ):

            return (
                True,
                package_id,
                f"{tool_name} is already up to date."
            )

        return (
            False,
            None,
            f"Unable to update {tool_name} "
            f"automatically using WinGet.\n"
            f"{output}"
        )

    # =================================================
    # Git automated installation/update
    # =================================================

    @classmethod
    def install_git(cls):
        """Automatically install Git using WinGet."""

        if platform.system() != "Windows":

            return (
                False,
                None,
                "Git automatic installation is "
                "supported on Windows only."
            )

        return cls.install_with_winget(
            "Git"
        )

    @classmethod
    def update_git(cls):
        """Automatically update Git using WinGet."""

        if platform.system() != "Windows":

            return (
                False,
                None,
                "Git automatic update is "
                "supported on Windows only."
            )

        return cls.update_with_winget(
            "Git"
        )

    # =================================================
    # Python automated installation/update
    # =================================================

    @classmethod
    def install_python(cls):
        """Automatically install Python 3.12 using WinGet."""

        if platform.system() != "Windows":

            return (
                False,
                None,
                "Python automatic installation is "
                "supported on Windows only."
            )

        return cls.install_with_winget(
            "Python"
        )

    @classmethod
    def update_python(cls):
        """
        Automatically update Python 3.12 using WinGet.

        This manages the system Python installation.
        The eSim Companion virtual environment is not
        replaced while the application is running.
        """

        if platform.system() != "Windows":

            return (
                False,
                None,
                "Python automatic update is "
                "supported on Windows only."
            )

        return cls.update_with_winget(
            "Python"
        )

    # =================================================
    # Git official installer fallback
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
        """
        Download the latest official Git x64 installer.

        This remains available as a fallback for the
        existing application functionality.
        """

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

            if destination.exists():

                try:

                    destination.unlink()

                except OSError:

                    return None

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
        Automatically install KiCad using WinGet.

        After installation, the installed KiCad executable
        is detected and saved in ConfigManager.
        """

        if platform.system() != "Windows":

            return (
                False,
                None,
                "KiCad automatic installation is "
                "supported on Windows only."
            )

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

        success, package_id, message = (
            cls.install_with_winget(
                "KiCad"
            )
        )

        if not success:

            return (
                False,
                None,
                message
            )

        executable = (
            cls.get_kicad_installed_executable()
        )

        if not executable:

            return (
                False,
                None,
                "KiCad installation completed, "
                "but the installed executable "
                "could not be detected."
            )

        ConfigManager.set_path(
            "KiCad",
            str(
                executable
            )
        )

        return (
            True,
            str(
                executable
            ),
            "KiCad installed automatically "
            "and verified successfully."
        )

    @classmethod
    def update_kicad(cls):
        """
        Automatically update KiCad using WinGet.

        After the update, the installed executable is
        detected and the configuration path is refreshed.
        """

        if platform.system() != "Windows":

            return (
                False,
                None,
                "KiCad automatic update is "
                "supported on Windows only."
            )

        success, package_id, message = (
            cls.update_with_winget(
                "KiCad"
            )
        )

        if not success:

            return (
                False,
                None,
                message
            )

        executable = (
            cls.get_kicad_installed_executable()
        )

        if executable:

            ConfigManager.set_path(
                "KiCad",
                str(
                    executable
                )
            )

            return (
                True,
                str(
                    executable
                ),
                message
            )

        return (
            True,
            None,
            message
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
        """
        Download the latest official Ngspice Windows
        64-bit package.
        """

        (
            latest_version,
            download_url,
            archive_name
        ) = cls.get_latest_ngspice_info()

        if not latest_version:

            return None

        return cls.download_file(
            download_url,
            archive_name
        )

    # =================================================
    # Ngspice latest version detection
    # =================================================

    @classmethod
    def _get_url_text(cls, url):
        """
        Retrieve text from a web page.

        urllib is attempted first.

        If the request is rejected or the returned page
        cannot be read correctly, Windows curl.exe is used
        as a fallback.

        Returns:
            str or None
        """

        if not url:
            return None

        user_agent = (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "eSim-Companion"
        )

        # -------------------------------------------------
        # First attempt: urllib
        # -------------------------------------------------

        try:

            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": user_agent,
                    "Accept": (
                        "text/html,"
                        "application/xhtml+xml,"
                        "application/xml;q=0.9,"
                        "*/*;q=0.8"
                    ),
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=cls.TIMEOUT
            ) as response:

                content = response.read()

            return content.decode(
                "utf-8",
                errors="ignore"
            )

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            OSError
        ):
            pass

        # -------------------------------------------------
        # Second attempt: curl
        # -------------------------------------------------

        curl_command = shutil.which(
            "curl.exe"
        )

        if not curl_command:
            return None

        try:

            result = subprocess.run(
                [
                    curl_command,
                    "-L",
                    "--fail",
                    "--silent",
                    "--show-error",
                    "--connect-timeout",
                    "30",
                    "--max-time",
                    str(cls.TIMEOUT),
                    "-A",
                    user_agent,
                    url,
                ],
                capture_output=True,
                text=True,
                timeout=cls.TIMEOUT + 10,
                stdin=subprocess.DEVNULL,
                creationflags=(
                    subprocess.CREATE_NO_WINDOW
                    if os.name == "nt"
                    else 0
                )
            )

            if result.returncode != 0:
                return None

            if not result.stdout:
                return None

            return result.stdout

        except (
            subprocess.SubprocessError,
            OSError
        ):

            return None

    @classmethod
    def _extract_ngspice_versions(cls, html):
        """
        Extract Ngspice Windows 64-bit release versions
        from SourceForge HTML.
        """

        if not html:
            return []

        patterns = [
            r"ngspice-(\d+(?:\.\d+)*)_64\.7z",
            r"ngspice-(\d+(?:\.\d+)*)%5F64\.7z",
        ]

        versions = set()

        for pattern in patterns:

            matches = re.findall(
                pattern,
                html,
                re.IGNORECASE
            )

            for version in matches:

                versions.add(
                    version
                )

        return sorted(
            versions,
            key=lambda value: tuple(
                int(part)
                for part in value.split(".")
            ),
            reverse=True
        )

    @classmethod
    def get_latest_ngspice_info(cls):
        """
        Find the latest official Ngspice Windows 64-bit
        release from the official SourceForge project.

        SourceForge can occasionally return a temporary
        error, incomplete page, or redirect response.
        Therefore the official page is checked several
        times before failing.

        Returns:
            (
                latest_version,
                download_url,
                archive_name
            )
        """

        if platform.system() != "Windows":

            return (
                None,
                None,
                None
            )

        page_url = (
            cls.DOWNLOAD_PAGES["Ngspice"]
        )

        # -------------------------------------------------
        # Retry the official source when the first request
        # does not contain a detectable release.
        # -------------------------------------------------

        for attempt in range(
            cls.NGSPICE_VERSION_CHECK_RETRIES
        ):

            html = cls._get_url_text(
                page_url
            )

            if html:

                versions = (
                    cls._extract_ngspice_versions(
                        html
                    )
                )

                if versions:

                    latest_version = (
                        versions[0]
                    )

                    archive_name = (
                        f"ngspice-"
                        f"{latest_version}"
                        f"_64.7z"
                    )

                    download_url = (
                        "https://sourceforge.net/"
                        "projects/ngspice/files/"
                        "ng-spice-rework/"
                        f"{latest_version}/"
                        f"{archive_name}/download"
                    )

                    return (
                        latest_version,
                        download_url,
                        archive_name
                    )

            # -------------------------------------------------
            # Wait before retrying.
            # -------------------------------------------------

            if (
                attempt
                < cls.NGSPICE_VERSION_CHECK_RETRIES - 1
            ):

                time.sleep(
                    cls.NGSPICE_RETRY_DELAY
                )

        return (
            None,
            None,
            None
        )

    @classmethod
    def get_latest_ngspice_version(cls):
        """Return the latest official Ngspice version."""

        version, _, _ = (
            cls.get_latest_ngspice_info()
        )

        return version

    # =================================================
    # Ngspice version helpers
    # =================================================

    @classmethod
    def get_installed_ngspice_version(cls):
        """
        Detect the installed Ngspice version using
        ngspice_con.exe -v.
        """

        executable = (
            cls.get_ngspice_console_executable()
        )

        if not executable:
            return None

        try:

            result = subprocess.run(
                [
                    str(executable),
                    "-v"
                ],
                capture_output=True,
                text=True,
                timeout=10,
                stdin=subprocess.DEVNULL,
                creationflags=(
                    subprocess.CREATE_NO_WINDOW
                    if os.name == "nt"
                    else 0
                )
            )

            output = (
                result.stdout
                or result.stderr
                or ""
            )

            match = re.search(
                r"ngspice[-\s]+"
                r"(\d+(?:\.\d+)*)",
                output,
                re.IGNORECASE
            )

            if not match:
                return None

            return match.group(1)

        except (
            subprocess.SubprocessError,
            OSError
        ):

            return None

    @staticmethod
    def _version_tuple(version):
        """Convert a version string into a comparable tuple."""

        if not version:
            return None

        try:

            return tuple(
                int(part)
                for part in version.split(".")
            )

        except (
            ValueError,
            AttributeError
        ):

            return None

    # =================================================
    # Ngspice extraction
    # =================================================

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

    # =================================================
    # Ngspice verification
    # =================================================

    @classmethod
    def verify_ngspice(
        cls,
        executable_path=None,
        expected_version=None
    ):
        """
        Verify Ngspice using the console executable.

        If expected_version is supplied, the detected
        version must match it.

        If expected_version is not supplied, any valid
        Ngspice version is accepted.
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
                timeout=10,
                stdin=subprocess.DEVNULL,
                creationflags=(
                    subprocess.CREATE_NO_WINDOW
                    if os.name == "nt"
                    else 0
                )
            )

            output = (
                result.stdout
                or result.stderr
                or ""
            )

            if result.returncode != 0:
                return False

            if "ngspice" not in output.lower():
                return False

            detected_version = (
                cls.get_installed_ngspice_version()
            )

            if not detected_version:
                return False

            if expected_version:

                detected_tuple = (
                    cls._version_tuple(
                        detected_version
                    )
                )

                expected_tuple = (
                    cls._version_tuple(
                        expected_version
                    )
                )

                if (
                    detected_tuple is None
                    or expected_tuple is None
                ):
                    return False

                return (
                    detected_tuple
                    == expected_tuple
                )

            return True

        except (
            subprocess.SubprocessError,
            OSError
        ):

            return False

    # =================================================
    # Ngspice automatic installation
    # =================================================

    @classmethod
    def install_ngspice(cls):
        """
        Automatically download, extract, verify, and
        configure the latest official Ngspice release.
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

            installed_version = (
                cls.get_installed_ngspice_version()
            )

            if installed_version:

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
                    (
                        "Ngspice is already installed "
                        f"(version {installed_version})."
                    )
                )

        # =================================================
        # Find latest official release
        # =================================================

        (
            latest_version,
            download_url,
            archive_name
        ) = cls.get_latest_ngspice_info()

        if not latest_version:

            return (
                False,
                None,
                "Unable to determine the latest "
                "official Ngspice release."
            )

        # =================================================
        # Download
        # =================================================

        archive_path = cls.download_file(
            download_url,
            archive_name
        )

        if not archive_path:

            return (
                False,
                None,
                (
                    "Unable to download "
                    f"Ngspice {latest_version}."
                )
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
                (
                    f"Ngspice {latest_version} "
                    "could not be extracted."
                )
            )

        # =================================================
        # Verify exact version
        # =================================================

        if not cls.verify_ngspice(
            console_executable,
            expected_version=latest_version
        ):

            return (
                False,
                None,
                (
                    f"Ngspice {latest_version} was "
                    "extracted but could not be verified."
                )
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
            (
                f"Ngspice {latest_version} "
                "installed successfully."
            )
        )

    # =================================================
    # Ngspice automatic update
    # =================================================

    @classmethod
    def update_ngspice(cls):
        """
        Automatically update Ngspice to the latest
        official Windows 64-bit release.

        Process:

        1. Detect installed version.
        2. Detect latest official version.
        3. Compare versions.
        4. Download only when a newer version exists.
        5. Extract the newer release.
        6. Verify the new version.
        7. Save the verified executable path.

        If the official version check temporarily fails,
        the existing installation is left untouched.
        """

        if platform.system() != "Windows":

            return (
                False,
                None,
                "Ngspice automatic update is "
                "supported on Windows only."
            )

        # =================================================
        # Detect installed executable
        # =================================================

        current_executable = (
            cls.get_ngspice_console_executable()
        )

        if not current_executable:

            return (
                False,
                None,
                "Ngspice is not currently installed."
            )

        # =================================================
        # Detect installed version
        # =================================================

        installed_version = (
            cls.get_installed_ngspice_version()
        )

        if not installed_version:

            return (
                False,
                str(current_executable),
                "Unable to determine the "
                "installed Ngspice version."
            )

        # =================================================
        # Detect latest official version
        # =================================================

        (
            latest_version,
            download_url,
            archive_name
        ) = cls.get_latest_ngspice_info()

        if not latest_version:

            return (
                False,
                str(current_executable),
                (
                    "Unable to determine the latest "
                    "official Ngspice version. "
                    "The existing installation was "
                    "not changed."
                )
            )

        # =================================================
        # Compare versions
        # =================================================

        installed_tuple = (
            cls._version_tuple(
                installed_version
            )
        )

        latest_tuple = (
            cls._version_tuple(
                latest_version
            )
        )

        if (
            installed_tuple is None
            or latest_tuple is None
        ):

            return (
                False,
                str(current_executable),
                "Unable to compare Ngspice versions."
            )

        # =================================================
        # Already up to date
        # =================================================

        if latest_tuple <= installed_tuple:

            ConfigManager.set_path(
                "Ngspice",
                str(current_executable)
            )

            return (
                True,
                str(current_executable),
                (
                    "Ngspice is already up to date "
                    f"(version {installed_version})."
                )
            )

        # =================================================
        # Download newer release
        # =================================================

        installer_path = cls.download_file(
            download_url,
            archive_name
        )

        if not installer_path:

            return (
                False,
                str(current_executable),
                (
                    f"Unable to download Ngspice "
                    f"{latest_version}. "
                    "The existing installation "
                    "was not changed."
                )
            )

        # =================================================
        # Extract newer release
        # =================================================

        extracted_executable = (
            cls.extract_ngspice(
                installer_path
            )
        )

        if not extracted_executable:

            return (
                False,
                str(current_executable),
                (
                    f"Ngspice {latest_version} "
                    "could not be extracted. "
                    "The existing installation "
                    "was not changed."
                )
            )

        # =================================================
        # Verify exact new version
        # =================================================

        if not cls.verify_ngspice(
            extracted_executable,
            expected_version=latest_version
        ):

            return (
                False,
                str(current_executable),
                (
                    f"Ngspice {latest_version} was "
                    "downloaded and extracted, but "
                    "verification failed."
                )
            )

        # =================================================
        # Save verified configuration
        # =================================================

        ConfigManager.set_path(
            "Ngspice",
            extracted_executable
        )

        return (
            True,
            extracted_executable,
            (
                f"Ngspice updated successfully "
                f"from {installed_version} "
                f"to {latest_version}."
            )
        )