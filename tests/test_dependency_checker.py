from services.dependency_checker import DependencyChecker


def main():

    checker = DependencyChecker()

    results = checker.check_all()

    print("\n===== eSim Companion Dependency Scan =====\n")

    for result in results:

        print(f"Tool       : {result.name}")
        print(f"Installed  : {result.installed}")
        print(f"Version    : {result.version}")
        print(f"Path       : {result.path}")
        print(f"Status     : {result.status}")
        print(f"Compatible : {result.compatible}")
        print(f"Message    : {result.message}")
        print("-" * 50)


if __name__ == "__main__":
    main()