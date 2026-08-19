"""
------------------------------------------------------------
File Name : dependency_checker.py

Purpose:
Detect installed tools, versions, paths, and compatibility
on the system.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import os
import re
import shutil
import subprocess

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from packaging.version import Version, InvalidVersion

from config.config_manager import ConfigManager
from config.tools import TOOLS


@dataclass
class ToolResult:
    """Represents the result of checking one tool."""

    name: str
    installed: bool
    version: Optional[str]
    path: Optional[str]
    status: str
    message: str
    compatible: Optional[bool]


class DependencyChecker:
    """Checks whether required external tools are available."""

    def __init__(self):
        self.tools = {
            tool["name"]: {
                "command": tool["command"],
                "version_args": tool["version_args"],
                "minimum_version": tool["minimum_version"],
            }
            for tool in TOOLS
        }

    # -------------------------------------------------
    # Check all tools
    # -------------------------------------------------

    def check_all(self):
        """Check every configured tool."""

        results = []

        for name, config in self.tools.items():

            result = self.check_tool(
                name,
                config["command"],
                config["version_args"]
            )

            results.append(result)

        return results

    # -------------------------------------------------
    # Find managed Python
    # -------------------------------------------------

    @staticmethod
    def find_python_executable():
        """
        Find the system Python 3.12 installation managed by
        the configured WinGet package.

        The active virtual environment is deliberately not
        selected because it belongs to eSim Companion itself.
        """

        if not platform_is_windows():
            return None

        # -------------------------------------------------
        # Prefer Windows Python Launcher.
        # -------------------------------------------------

        py_launcher = shutil.which(
            "py.exe"
        )

        if py_launcher:

            try:

                result = subprocess.run(
                    [
                        py_launcher,
                        "-3.12",
                        "-c",
                        "import sys; print(sys.executable)"
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    stdin=subprocess.DEVNULL,
                    creationflags=(
                        subprocess.CREATE_NO_WINDOW
                        if os.name == "nt"
                        else 0
                    )
                )

                path = result.stdout.strip()

                if (
                    path
                    and os.path.isfile(path)
                ):

                    return path

            except (
                subprocess.SubprocessError,
                OSError
            ):

                pass

        # -------------------------------------------------
        # Fallback:
        # Standard per-user Python 3.12 installation.
        # -------------------------------------------------

        local_app_data = os.environ.get(
            "LocalAppData"
        )

        if local_app_data:

            fallback = (
                Path(local_app_data)
                / "Programs"
                / "Python"
                / "Python312"
                / "python.exe"
            )

            if fallback.is_file():

                return str(
                    fallback
                )

        # -------------------------------------------------
        # Fallback:
        # Standard system-wide Python 3.12 installation.
        # -------------------------------------------------

        program_files = os.environ.get(
            "ProgramFiles"
        )

        if program_files:

            fallback = (
                Path(program_files)
                / "Python312"
                / "python.exe"
            )

            if fallback.is_file():

                return str(
                    fallback
                )

        return None

    # -------------------------------------------------
    # Find KiCad
    # -------------------------------------------------

    @staticmethod
    def find_kicad_executable():
        """
        Find the installed KiCad executable on Windows.

        KiCad is normally installed under:

        C:\\Program Files\\KiCad\\10.0\\bin\\kicad.exe

        KiCad may not be added to PATH, so shutil.which()
        cannot reliably detect it.
        """

        if not platform_is_windows():
            return None

        possible_roots = []

        program_files = os.environ.get(
            "ProgramFiles"
        )

        program_w6432 = os.environ.get(
            "ProgramW6432"
        )

        if program_files:

            possible_roots.append(
                Path(program_files)
                / "KiCad"
            )

        if program_w6432:

            possible_roots.append(
                Path(program_w6432)
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

                return str(
                    executables[0]
                )

        return None

    # -------------------------------------------------
    # Check one tool
    # -------------------------------------------------

    def check_tool(
        self,
        name,
        command,
        version_args
    ):
        """Check whether a specific tool is installed."""

        configured_path = (
            ConfigManager.get_path(
                name
            )
        )

        # -------------------------------------------------
        # Python is managed separately from the project's
        # virtual environment.
        # -------------------------------------------------

        if name == "Python":

            path = (
                self.find_python_executable()
            )

        else:

            # -------------------------------------------------
            # Use configured path first.
            # -------------------------------------------------

            if (
                configured_path
                and os.path.isfile(
                    configured_path
                )
            ):

                path = configured_path

            else:

                path = shutil.which(
                    command
                )

        # -------------------------------------------------
        # Special handling for KiCad.
        # -------------------------------------------------

        if (
            path is None
            and name == "KiCad"
        ):

            path = (
                self.find_kicad_executable()
            )

        # -------------------------------------------------
        # If a tool was found, save the resolved path.
        #
        # This is important for Git because Git is normally
        # detected through PATH and was previously not saved
        # to tool_paths.json.
        # -------------------------------------------------

        if path:

            try:

                if os.path.isfile(path):

                    ConfigManager.set_path(
                        name,
                        str(path)
                    )

            except OSError:

                pass

        minimum_version = (
            self.tools[name]["minimum_version"]
        )

        # -------------------------------------------------
        # Tool not found.
        # -------------------------------------------------

        if path is None:

            return ToolResult(
                name=name,
                installed=False,
                version=None,
                path=None,
                status="Missing",
                message=(
                    f"{name} was not found on this system."
                ),
                compatible=False
            )

        # -------------------------------------------------
        # Tool found.
        # -------------------------------------------------

        version = self.get_version(
            path,
            version_args
        )

        # -------------------------------------------------
        # Check compatibility.
        # -------------------------------------------------

        compatible = (
            self.check_compatibility(
                version,
                minimum_version
            )
        )

        # -------------------------------------------------
        # Incompatible.
        # -------------------------------------------------

        if (
            minimum_version
            and not compatible
        ):

            return ToolResult(
                name=name,
                installed=True,
                version=version,
                path=path,
                status="Incompatible",
                message=(
                    f"{name} version is below the "
                    f"required version "
                    f"{minimum_version}."
                ),
                compatible=False
            )

        # -------------------------------------------------
        # Installed.
        # -------------------------------------------------

        return ToolResult(
            name=name,
            installed=True,
            version=version,
            path=path,
            status="Installed",
            message=(
                f"{name} detected successfully."
            ),
            compatible=True
        )

    # -------------------------------------------------
    # Compatibility
    # -------------------------------------------------

    def check_compatibility(
        self,
        version,
        minimum_version
    ):
        """Check whether an installed version meets the minimum version."""

        if not minimum_version:
            return True

        if (
            not version
            or version == "Unknown"
        ):

            return False

        try:

            actual_version = (
                self.extract_version(
                    version
                )
            )

            return (
                Version(actual_version)
                >= Version(minimum_version)
            )

        except InvalidVersion:

            return False

    # -------------------------------------------------
    # Extract version
    # -------------------------------------------------

    @staticmethod
    def extract_version(version_output):
        """Extract a meaningful software version from command output."""

        if not version_output:

            raise InvalidVersion(
                "Empty version output"
            )

        # -------------------------------------------------
        # Ngspice-specific version format.
        # -------------------------------------------------

        ngspice_match = re.search(
            r"ngspice[-\s]+(\d+(?:\.\d+)*)",
            version_output,
            re.IGNORECASE
        )

        if ngspice_match:

            return (
                ngspice_match.group(1)
            )

        # -------------------------------------------------
        # Normal semantic version.
        # -------------------------------------------------

        match = re.search(
            r"\d+\.\d+(?:\.\d+)*",
            version_output
        )

        if match:

            return match.group(0)

        # -------------------------------------------------
        # Simple version.
        # -------------------------------------------------

        simple_match = re.search(
            r"\b(\d+)\b",
            version_output
        )

        if simple_match:

            return (
                simple_match.group(1)
            )

        raise InvalidVersion(
            version_output
        )

    # -------------------------------------------------
    # Get version
    # -------------------------------------------------

    @staticmethod
    def get_version(
        command,
        version_args
    ):
        """
        Retrieve and normalize the installed version.

        Ngspice uses ngspice_con.exe.

        KiCad uses kicad-cli.exe because kicad.exe is
        graphical.
        """

        try:

            command_path = Path(
                command
            )

            # -------------------------------------------------
            # Ngspice.
            # -------------------------------------------------

            if (
                command_path.name.lower()
                == "ngspice.exe"
            ):

                console_executable = (
                    command_path.parent
                    / "ngspice_con.exe"
                )

                if console_executable.is_file():

                    command = str(
                        console_executable
                    )

                    version_args = [
                        "-v"
                    ]

            # -------------------------------------------------
            # KiCad.
            # -------------------------------------------------

            elif (
                command_path.name.lower()
                == "kicad.exe"
            ):

                cli_executable = (
                    command_path.parent
                    / "kicad-cli.exe"
                )

                if cli_executable.is_file():

                    command = str(
                        cli_executable
                    )

                    version_args = [
                        "--version"
                    ]

            # -------------------------------------------------
            # Run version command.
            # -------------------------------------------------

            result = subprocess.run(
                [
                    command
                ] + version_args,
                capture_output=True,
                text=True,
                timeout=5,
                stdin=subprocess.DEVNULL,
                creationflags=(
                    subprocess.CREATE_NO_WINDOW
                    if os.name == "nt"
                    else 0
                )
            )

            output = (
                result.stdout.strip()
                or result.stderr.strip()
            )

            return (
                DependencyChecker.extract_version(
                    output
                )
            )

        except (
            subprocess.SubprocessError,
            OSError,
            InvalidVersion
        ):

            return "Unknown"


# -------------------------------------------------
# Platform helper
# -------------------------------------------------

def platform_is_windows():
    """Return True when running on Windows."""

    return os.name == "nt"