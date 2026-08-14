from services.update_checker import UpdateChecker


def main():

    print("===== All Tools Latest Version Test =====")

    tools = [
        "Python",
        "Git",
        "Ngspice",
        "KiCad"
    ]

    for tool in tools:

        latest = UpdateChecker.get_latest_version(
            tool
        )

        print(
            f"{tool} latest version: {latest}"
        )


if __name__ == "__main__":
    main()