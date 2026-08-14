import customtkinter as ctk

from gui.layouts.activity_layout import ActivityLayout


def main():

    app = ctk.CTk()

    app.title("eSim Companion - Activity Test")
    app.geometry("1100x750")

    activities = [
        "Application started",
        "Environment scan completed",
        "Python detected",
        "Git detected",
        "Ngspice not found",
        "KiCad not found"
    ]

    activity = ActivityLayout(
        app,
        activities=activities
    )

    activity.pack(
        fill="both",
        expand=True
    )

    app.mainloop()


if __name__ == "__main__":
    main()