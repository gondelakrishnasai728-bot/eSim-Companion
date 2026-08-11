import customtkinter as ctk

from gui.layouts.scanner_layout import ScannerLayout


def main():
    app = ctk.CTk()

    app.title("eSim Companion - Scanner Test")
    app.geometry("1100x750")

    scanner = ScannerLayout(app)

    scanner.pack(
        fill="both",
        expand=True
    )

    app.mainloop()


if __name__ == "__main__":
    main()