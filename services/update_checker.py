"""
------------------------------------------------------------
File Name : update_checker.py

Purpose:
Checks whether installed tools have newer versions available.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

import json
import re
import urllib.request

from packaging.version import Version, InvalidVersion


class UpdateChecker:
    """Checks installed versions against latest versions."""

    TIMEOUT = 5

    SOURCES = {
        "Git": {
            "url": (
                "https://api.github.com/repos/"
                "git-for-windows/git/releases/latest"
            ),
            "version_key": "tag_name"
        },

        "Python": {
            "url": (
                "https://www.python.org/api/v2/"
                "downloads/release/"
                "?is_published=true"
                "&sort=-release_date"
            ),
            "version_key": "name"
        },
        "KiCad": {
            "url": (
                "https://gitlab.com/api/v4/projects/"
                "kicad%2Fcode%2Fkicad/repository/tags"
                "?per_page=100"
                "&order_by=updated"
                "&sort=desc"
            ),
            "version_key": "name"
        }
    }

    @staticmethod
    def compare_versions(installed, latest):
        """Compare two version strings."""

        if not installed or not latest:
            return "Unknown"

        try:
            # Git for Windows versions can look like:
            # 2.55.0.windows.4
            #
            # Compare the main numeric version.
            installed_normalized = (
                installed.split(".windows")[0]
            )

            latest_normalized = (
                latest.split(".windows")[0]
            )

            installed_version = Version(
                installed_normalized
            )

            latest_version = Version(
                latest_normalized
            )

        except InvalidVersion:
            return "Unknown"

        if installed_version < latest_version:
            return "Update Available"

        if installed_version == latest_version:
            return "Up to Date"

        return "Newer Than Latest"

    @staticmethod
    def fetch_json(url):
        """Fetch JSON data from a URL."""

        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "eSim-Companion"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=UpdateChecker.TIMEOUT
            ) as response:

                data = response.read().decode(
                    "utf-8"
                )

                return json.loads(data)

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            json.JSONDecodeError,
            OSError
        ):
            return None

    @classmethod
    def get_latest_version(cls, tool_name):
        """Retrieve the latest available version."""

        # Python has a different API response format.
        if tool_name == "Python":
            return cls.get_python_latest_version()
        if tool_name == "Ngspice":
            return cls.get_ngspice_latest_version()
        if tool_name == "KiCad":
            return cls.get_kicad_latest_version()

        source = cls.SOURCES.get(tool_name)

        if not source:
            return None

        data = cls.fetch_json(
            source["url"]
        )

        if not isinstance(data, dict):
            return None

        version = data.get(
            source["version_key"]
        )

        if not version:
            return None

        if version.startswith("v"):
            version = version[1:]

        return version

    @classmethod
    def get_python_latest_version(cls):
        """Retrieve the latest stable Python 3 release."""

        url = (
            "https://www.python.org/api/v2/"
            "downloads/release/"
            "?is_published=true"
            "&pre_release=false"
            "&sort=-release_date"
            "&limit=100"
        )

        data = cls.fetch_json(url)

        if not isinstance(data, list):
            return None

        versions = []

        for release in data:

            name = release.get("name")

            if not name:
                continue

            if not name.startswith("Python 3."):
                continue

            version = name.replace(
                "Python ",
                ""
            ).strip()

            try:
                parsed_version = Version(
                    version
                )

            except InvalidVersion:
                continue

            versions.append(
                parsed_version
            )

        if not versions:
            return None

        latest = max(versions)

        return str(latest)
    @classmethod
    def get_ngspice_latest_version(cls):
        """Retrieve the latest Ngspice release version."""

        url = (
            "https://sourceforge.net/projects/"
            "ngspice/files/ng-spice-rework/"
        )

        try:
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

                html = response.read().decode(
                    "utf-8",
                    errors="ignore"
                )

            import re

            versions = re.findall(
                r"ngspice[-_](\d+)",
                html,
                re.IGNORECASE
            )

            if not versions:
                return None

            return str(
                max(
                    int(version)
                    for version in versions
                )
            )

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            OSError
        ):
            return None
    @classmethod
    def get_kicad_latest_version(cls):
        """Retrieve the latest stable KiCad 10 release."""

        url = (
            "https://gitlab.com/api/v4/projects/"
            "kicad%2Fcode%2Fkicad/repository/tags"
            "?per_page=100"
            "&order_by=updated"
            "&sort=desc"
        )

        data = cls.fetch_json(url)

        if not isinstance(data, list):
            return None

        versions = []

        for tag in data:

            name = tag.get("name")

            if not name:
                continue

            # Only accept stable KiCad 10.0.x releases.
            #
            # Examples accepted:
            # 10.0.0
            # 10.0.4
            # 10.0.5
            #
            # Examples rejected:
            # 10.0.5-rc1
            # 10.99.0
            # development versions

            if not re.fullmatch(
                r"10\.0\.\d+",
                name
            ):
                continue

            try:
                version = Version(name)

            except InvalidVersion:
                continue

            versions.append(version)

        if not versions:
            return None

        latest = max(versions)

        return str(latest)