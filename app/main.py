"""
------------------------------------------------------------
File Name : main.py

Purpose :
Entry point of the eSim Companion application.

Author : Krishna Sai
------------------------------------------------------------
"""

import customtkinter as ctk

from gui.components.status_card import StatusCard
from utils.theme import Theme


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(Theme.Window.TITLE)

        self.geometry(
            f"{Theme.Sizes.WINDOW_WIDTH}x{Theme.Sizes.WINDOW_HEIGHT}"
        )

        self.configure(
            fg_color=Theme.Colors.BACKGROUND
        )

        self.create_widgets()

    def create_widgets(self):

        python_card = StatusCard(
            self,
            title="🐍 Python",
            version="3.12.10",
            status="Installed"
        )

        python_card.pack(
            padx=40,
            pady=40
        )


if __name__ == "__main__":

    ctk.set_appearance_mode("Dark")

    ctk.set_default_color_theme("blue")

    app = MainWindow()

    app.mainloop()