from services.activity_manager import ActivityManager


def main():

    print("===== Activity Manager Test =====")

    ActivityManager.clear_activity()

    print(
        "Initial:",
        ActivityManager.get_activities()
    )

    ActivityManager.add_activity(
        "Test activity recorded"
    )

    ActivityManager.add_activity(
        "Second activity recorded"
    )

    print(
        "After adding:",
        ActivityManager.get_activities()
    )

    ActivityManager.clear_activity()

    print(
        "After clearing:",
        ActivityManager.get_activities()
    )


if __name__ == "__main__":
    main()