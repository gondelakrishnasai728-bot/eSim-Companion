"""
------------------------------------------------------------
File Name : status_card.py

Purpose :
Displays the status of a software tool
(Python, Git, Ngspice, KiCad).

Author : Krishna Sai
------------------------------------------------------------
"""

import customtkinter as ctk

from gui.components.base_card import BaseCard
from utils.theme import Theme


class StatusCard(BaseCard):
    """
    Displays information about a software tool.
    """

    def __init__(self, parent, title, version, status):

        super().__init__(parent)

        self.title = title
        self.version = version
        self.status = status

        self.create_widgets()

    def create_widgets(self):

        title_label = ctk.CTkLabel(
            self,
            text=self.title,
            font=Theme.Fonts.HEADING,
            text_color=Theme.Colors.TEXT,
        )

        title_label.pack(
            anchor="w",
            padx=Theme.Spacing.MEDIUM,
            pady=(15, 5),
        )

        version_label = ctk.CTkLabel(
            self,
            text=f"Version : {self.version}",
            font=Theme.Fonts.BODY,
            text_color=Theme.Colors.SUBTEXT,
        )

        version_label.pack(
            anchor="w",
            padx=Theme.Spacing.MEDIUM,
        )

        status_color = Theme.Colors.SUCCESS

        if self.status.lower() == "missing":
            status_color = Theme.Colors.ERROR

        elif self.status.lower() in [
            "update available",
            "incompatible"
            ]:
            status_color = Theme.Colors.WARNING

        status_label = ctk.CTkLabel(
            self,
            text=f"Status : {self.status}",
            font=Theme.Fonts.BODY,
            text_color=status_color,
            )

        status_label.pack(
            anchor="w",
            padx=Theme.Spacing.MEDIUM,
            pady=(10, 0),
        )