"""
------------------------------------------------------------
File Name : tools.py

Purpose:
Defines the external tools managed by eSim Companion
and their compatibility requirements.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

TOOLS = [
    {
        "name": "Python",
        "display_name": "🐍 Python",
        "command": "python",
        "version_args": ["--version"],
        "minimum_version": "3.12.0",
    },
    {
        "name": "Git",
        "display_name": "🌿 Git",
        "command": "git",
        "version_args": ["--version"],
        "minimum_version": "2.40.0",
    },
    {
        "name": "Ngspice",
        "display_name": "⚡ Ngspice",
        "command": "ngspice",
        "version_args": ["--version"],
        "minimum_version": None,
    },
    {
        "name": "KiCad",
        "display_name": "🛠 KiCad",
        "command": "kicad",
        "version_args": ["--version"],
        "minimum_version": None,
    },
]