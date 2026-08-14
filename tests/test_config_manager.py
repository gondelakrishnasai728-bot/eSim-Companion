from config.config_manager import ConfigManager


def main():

    print("===== Config Manager Test =====")

    config = ConfigManager.load_config()

    print("Current configuration:")
    print(config)

    ConfigManager.set_path(
        "Ngspice",
        r"C:\Test\ngspice.exe"
    )

    print()
    print(
        "Ngspice path:",
        ConfigManager.get_path("Ngspice")
    )


if __name__ == "__main__":
    main()