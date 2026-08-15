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
    # Check one tool
    # -------------------------------------------------

    def check_tool(self, name, command, version_args):
        """Check whether a specific tool is installed."""

        configured_path = ConfigManager.get_path(name)

        if (
            configured_path
            and os.path.isfile(configured_path)
        ):
            path = configured_path
        else:
            path = shutil.which(command)

        minimum_version = self.tools[name]["minimum_version"]

        # -------------------------------------------------
        # Tool not found
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
        # Tool found
        # -------------------------------------------------

        version = self.get_version(
            path,
            version_args
        )

        # -------------------------------------------------
        # Check compatibility
        # -------------------------------------------------

        compatible = self.check_compatibility(
            version,
            minimum_version
        )

        # -------------------------------------------------
        # Incompatible
        # -------------------------------------------------

        if minimum_version and not compatible:

            return ToolResult(
                name=name,
                installed=True,
                version=version,
                path=path,
                status="Incompatible",
                message=(
                    f"{name} version is below the "
                    f"required version {minimum_version}."
                ),
                compatible=False
            )

        # -------------------------------------------------
        # Installed
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

        # No minimum version configured
        if not minimum_version:
            return True

        # No version detected
        if not version or version == "Unknown":
            return False

        try:

            actual_version = self.extract_version(
                version
            )

            return Version(actual_version) >= Version(
                minimum_version
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
        # Ngspice-specific version format
        #
        # Example:
        # ngspice-46
        # -------------------------------------------------

        ngspice_match = re.search(
            r"ngspice[-\s]+(\d+(?:\.\d+)*)",
            version_output,
            re.IGNORECASE
        )

        if ngspice_match:
            return ngspice_match.group(1)

        # -------------------------------------------------
        # Normal semantic version
        #
        # Examples:
        # 3.12.0
        # 2.40.0
        # 9.0
        # -------------------------------------------------

        match = re.search(
            r"\d+\.\d+(?:\.\d+)*",
            version_output
        )

        if match:
            return match.group(0)

        # -------------------------------------------------
        # Simple version such as:
        #
        # ngspice-46
        # -------------------------------------------------

        simple_match = re.search(
            r"\b(\d+)\b",
            version_output
        )

        if simple_match:
            return simple_match.group(1)

        raise InvalidVersion(
            version_output
        )

    # -------------------------------------------------
    # Get version
    # -------------------------------------------------

    @staticmethod
    def get_version(command, version_args):
        """
        Retrieve and normalize the installed version.

        Ngspice requires special handling because the normal
        ngspice.exe executable can open its graphical
        interface when queried incorrectly.

        The console executable ngspice_con.exe is therefore
        used for version detection.
        """

        try:

            command_path = Path(command)

            # -------------------------------------------------
            # Special handling for Ngspice
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

                    # The console executable can print
                    # its version without opening the GUI.
                    version_args = ["-v"]

            # -------------------------------------------------
            # Run version command
            # -------------------------------------------------

            result = subprocess.run(
                [command] + version_args,
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

            # -------------------------------------------------
            # Extract version
            # -------------------------------------------------

            return DependencyChecker.extract_version(
                output
            )

        except (
            subprocess.SubprocessError,
            OSError,
            InvalidVersion
        ):

            return "Unknown"