"""
------------------------------------------------------------
File Name : main.py

Purpose:
Application entry point for eSim Companion.

Author : Krishna Sai
Project : eSim Companion
------------------------------------------------------------
"""

from gui.main_window import create_application


if __name__ == "__main__":

    app = create_application()

    app.mainloop()