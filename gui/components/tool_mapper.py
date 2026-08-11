"""
------------------------------------------------------------
File Name : tool_mapper.py

Purpose:
Converts DependencyChecker results into data that can
be displayed by the dashboard.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

from config.tools import TOOLS


def get_display_name(tool_name):
    """Return the configured display name for a tool."""

    for tool in TOOLS:
        if tool["name"] == tool_name:
            return tool["display_name"]

    return tool_name

def result_to_card_data(result):
    """Convert a ToolResult into StatusCard-compatible data."""

    return {
        "name": get_display_name(result.name),
        "version": result.version or "Not detected",
        "status": result.status,
        "installed": result.installed,
        "compatible": result.compatible,
        "path": result.path,
        "message": result.message,
    }