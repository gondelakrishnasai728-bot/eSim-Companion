"""
------------------------------------------------------------
File Name : base_card.py

Purpose :
Provides a reusable base card component for all
dashboard cards in eSim Companion.

Author : Krishna Sai
------------------------------------------------------------
"""

import customtkinter as ctk
from utils.theme import Theme


class BaseCard(ctk.CTkFrame):
    """
    Base reusable card component.

    Other cards like StatusCard, HealthCard,
    ActionCard will inherit from this class.
    """

    def __init__(self, parent):

        super().__init__(
            master=parent,
            fg_color=Theme.Colors.CARD,
            corner_radius=Theme.Radius.LARGE,
            border_width=1,
            border_color=Theme.Colors.BORDER,
            width=Theme.Sizes.CARD_WIDTH,
            height=Theme.Sizes.CARD_HEIGHT,
        )

        self.pack_propagate(False)