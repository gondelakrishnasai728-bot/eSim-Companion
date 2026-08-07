"""
------------------------------------------------------------
File Name : constants.py

Purpose:
Stores all application-wide constants used throughout
the eSim Companion application.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""


class AppInfo:
    """General application information."""

    NAME = "eSim Companion"
    VERSION = "1.0.0"
    DESCRIPTION = "Smart Environment & Tool Manager for eSim"
    AUTHOR = "Krishna Sai"
    LICENSE = "MIT"


class SupportedOS:
    """Supported operating systems."""

    WINDOWS = "Windows"
    LINUX = "Linux"


class SupportedTools:
    """External tools managed by the application."""

    PYTHON = "Python"
    GIT = "Git"
    NGSPICE = "Ngspice"
    KICAD = "KiCad"


class Messages:
    """Common messages displayed in the application."""

    LOADING = "Loading application..."
    SCANNING = "Scanning system..."
    READY = "Environment Ready"
    INSTALLING = "Installing..."
    COMPLETED = "Operation Completed Successfully"
    FAILED = "Operation Failed"