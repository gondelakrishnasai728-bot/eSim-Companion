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

import re
import shutil
import subprocess

from dataclasses import dataclass
from typing import Optional

from packaging.version import Version, InvalidVersion

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

    def check_tool(self, name, command, version_args):
        """Check whether a specific tool is installed."""

        path = shutil.which(command)

        minimum_version = self.tools[name]["minimum_version"]

        # Tool not found
        if path is None:

            return ToolResult(
                name=name,
                installed=False,
                version=None,
                path=None,
                status="Missing",
                message=f"{name} was not found on this system.",
                compatible=False
            )

        # Tool found, retrieve version
        version = self.get_version(
            command,
            version_args
        )

        # Check compatibility
        compatible = self.check_compatibility(
            version,
            minimum_version
        )

        # Version is incompatible
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

        # Tool is installed and compatible
        return ToolResult(
            name=name,
            installed=True,
            version=version,
            path=path,
            status="Installed",
            message=f"{name} detected successfully.",
            compatible=True
        )

    def check_compatibility(self, version, minimum_version):
        """Check whether an installed version meets the minimum version."""

        # No minimum version configured
        if not minimum_version:
            return True

        # No version detected
        if not version:
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

    @staticmethod
    def extract_version(version_output):
        """Extract the numeric version from command output."""

        match = re.search(
            r"\d+(?:\.\d+)+",
            version_output
        )

        if not match:
            raise InvalidVersion(version_output)

        return match.group(0)

    @staticmethod
    def get_version(command, version_args):
        """Retrieve and normalize the installed version."""

        try:

            result = subprocess.run(
                [command] + version_args,
                capture_output=True,
                text=True,
                timeout=5
            )

            output = (
                result.stdout.strip()
                or result.stderr.strip()
            )

            return DependencyChecker.extract_version(
                output
            )

        except (
            subprocess.SubprocessError,
            OSError,
            InvalidVersion
        ):

            return "Unknown"