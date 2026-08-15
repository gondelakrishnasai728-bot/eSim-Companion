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
import urllib.error
import urllib.request

from packaging.version import Version, InvalidVersion


class UpdateChecker:
    """Checks installed versions against latest versions."""

    TIMEOUT = 10

    SOURCES = {
        "Git": {
            "url": (
                "https://api.github.com/repos/"
                "git-for-windows/git/releases/latest"
            ),
            "version_key": "tag_name",
        },
    }

    # =================================================
    # Version comparison
    # =================================================

    @staticmethod
    def normalize_version(version):
        """Normalize a tool version for comparison."""

        if not version:
            return None

        version = str(version).strip()

        # Remove common prefixes.
        version = version.lstrip("vV")

        # Git for Windows:
        # 2.53.0.windows.1 -> 2.53.0
        if ".windows" in version.lower():

            version = re.split(
                r"\.windows",
                version,
                flags=re.IGNORECASE
            )[0]

        # Remove common suffixes such as:
        # -rc1
        # -beta1
        version = re.split(
            r"[-+]",
            version,
            maxsplit=1
        )[0]

        return version.strip()

    @classmethod
    def compare_versions(cls, installed, latest):
        """Compare two version strings."""

        if not installed or not latest:
            return "Unknown"

        installed_normalized = cls.normalize_version(
            installed
        )

        latest_normalized = cls.normalize_version(
            latest
        )

        if not installed_normalized or not latest_normalized:
            return "Unknown"

        try:

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

    # =================================================
    # HTTP / JSON
    # =================================================

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

    # =================================================
    # Latest version dispatcher
    # =================================================

    @classmethod
    def get_latest_version(cls, tool_name):
        """Retrieve the latest available version."""

        if tool_name == "Python":

            return cls.get_python_latest_version()

        if tool_name == "Ngspice":

            return cls.get_ngspice_latest_version()

        if tool_name == "KiCad":

            return cls.get_kicad_latest_version()

        source = cls.SOURCES.get(
            tool_name
        )

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

        return cls.normalize_version(
            version
        )

    # =================================================
    # Python
    # =================================================

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

            if not isinstance(release, dict):
                continue

            name = release.get(
                "name"
            )

            if not name:
                continue

            if not name.startswith(
                "Python 3."
            ):
                continue

            version = name.replace(
                "Python ",
                "",
                1
            ).strip()

            try:

                parsed_version = Version(
                    version
                )

            except InvalidVersion:

                continue

            # Ignore prerelease versions.
            if parsed_version.is_prerelease:
                continue

            versions.append(
                parsed_version
            )

        if not versions:
            return None

        return str(
            max(versions)
        )

    # =================================================
    # Ngspice
    # =================================================

    @classmethod
    def get_ngspice_latest_version(cls):
        """Retrieve the latest stable Ngspice release version."""

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

            versions = re.findall(
                r"ngspice[-_](\d+)",
                html,
                re.IGNORECASE
            )

            if not versions:
                return None

            numeric_versions = [
                int(version)
                for version in versions
            ]

            return str(
                max(numeric_versions)
            )

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            OSError
        ):

            return None

    # =================================================
    # KiCad
    # =================================================

    @classmethod
    def get_kicad_latest_version(cls):
        """Retrieve the latest stable KiCad release version."""

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

            if not isinstance(tag, dict):
                continue

            name = tag.get(
                "name"
            )

            if not name:
                continue

            name = str(name).strip()

            # Remove a leading v.
            name = name.lstrip("vV")

            # Accept only stable numeric versions:
            #
            # 10.0.0
            # 10.0.1
            # 10.1.0
            # 9.0.0
            #
            # Reject:
            # 10.0.0-rc1
            # 10.0.0-beta
            # development tags
            # 10.99.x development versions

            if not re.fullmatch(
                r"\d+\.\d+\.\d+",
                name
            ):
                continue

            try:

                version = Version(
                    name
                )

            except InvalidVersion:

                continue

            # Ignore prerelease versions.
            if version.is_prerelease:
                continue

            # -------------------------------------------------
            # Ignore KiCad development versions.
            #
            # KiCad 10.99.x represents the development branch,
            # not a stable public release.
            # -------------------------------------------------

            parts = name.split(".")

            try:

                major = int(parts[0])
                minor = int(parts[1])

            except (
                ValueError,
                IndexError
            ):

                continue

            if major == 10 and minor >= 99:
                continue

            versions.append(
                version
            )

        if not versions:
            return None

        return str(
            max(versions)
        )