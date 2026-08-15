from services.tool_installer import ToolInstaller


print("===== Git Installer Launch Test =====")

installer = ToolInstaller.download_git_installer()

print(
    "Installer:",
    installer
)

if installer:

    launched = ToolInstaller.launch_installer(
        installer
    )

    print(
        "Installer launched:",
        launched
    )

else:

    print(
        "Installer download failed."
    )