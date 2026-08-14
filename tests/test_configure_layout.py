import customtkinter as ctk

from gui.layouts.configure_layout import ConfigureLayout


def main():

    app = ctk.CTk()

    app.title("eSim Companion - Configure Test")
    app.geometry("1100x750")

    configure = ConfigureLayout(app)

    configure.pack(
        fill="both",
        expand=True
    )

    app.mainloop()


if __name__ == "__main__":
    main()