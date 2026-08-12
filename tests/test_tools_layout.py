import customtkinter as ctk

from gui.layouts.tools_layout import ToolsLayout


def main():

    app = ctk.CTk()

    app.title("eSim Companion - Tools Test")
    app.geometry("1100x750")

    tools = ToolsLayout(app)

    tools.pack(
        fill="both",
        expand=True
    )

    app.mainloop()


if __name__ == "__main__":
    main()