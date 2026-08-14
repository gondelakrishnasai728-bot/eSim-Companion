from services.update_checker import UpdateChecker


def main():

    print("===== Ngspice Live Update Test =====")

    latest = UpdateChecker.get_ngspice_latest_version()

    print(
        "Latest Ngspice version:",
        latest
    )


if __name__ == "__main__":
    main()