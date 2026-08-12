"""
File Name : tool_installer.py

Purpose:
Handles installation actions for external eSim tools.
"""

import webbrowser


class ToolInstaller:
    """Handles installation actions for supported tools."""

    DOWNLOAD_PAGES = {
       "Git": "https://git-scm.com/install/windows",
        "Ngspice": "https://sourceforge.net/projects/ngspice/files/ng-spice-rework/",
        "KiCad": "https://www.kicad.org/download/",
    }

    @classmethod
    def open_download_page(cls, tool_name):
        """Open the official download page for a tool."""

        url = cls.DOWNLOAD_PAGES.get(tool_name)

        if not url:
            return False

        webbrowser.open(url)

        return True

