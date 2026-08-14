import customtkinter as ctk

from gui.layouts.updates_layout import UpdatesLayout


def main():

    app = ctk.CTk()

    app.title("eSim Companion - Updates Test")
    app.geometry("1100x750")

    updates = UpdatesLayout(app)

    updates.pack(
        fill="both",
        expand=True
    )

    app.mainloop()


if __name__ == "__main__":
    main()