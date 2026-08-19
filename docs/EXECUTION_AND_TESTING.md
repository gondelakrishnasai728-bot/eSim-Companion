# eSim Companion
## Execution and Testing Instructions

### Task 5 - Automated Tool Installation and Dependency Management

**Internship:** eSim Semester Long Internship - Autumn 2026
**Task:** Task 5 - Tool Manager
**Project:** eSim Companion
**Author:** Krishna Sai
**Platform:** Windows
**Language:** Python

---

# 1. Purpose

This document provides the steps required to install, execute, and test the eSim Companion Automated Tool Manager.

The Task 5 implementation provides automated management of the external tools required by the eSim environment:

- Python
- Git
- Ngspice
- KiCad

The application supports dependency detection, version checking, compatibility checking, installation, updates, configuration management, executable-path recovery, and a graphical Tool Manager.

The official Task 5 requirements specify that the execution instructions should provide clear steps for running and testing the prototype, including installation instructions for required dependencies.

---

# 2. System Requirements

## 2.1 Operating System

The current automated installation and update implementation is designed primarily for:

    Windows 10 / Windows 11

The implementation uses Windows Package Manager (WinGet) for selected tools.

Cross-platform installation using Linux or macOS package managers is not currently implemented.

## 2.2 Software Requirements

The development and testing environment contains:

| Component | Tested Version |
|-----------|----------------|
| Python | 3.12.10 |
| Git | 2.55.0 |
| Ngspice | 47 |
| KiCad | 10.0.5 |
| WinGet | Windows Package Manager |

## 2.3 Internet Connection

An internet connection is required for:

- Downloading packages through WinGet.
- Checking available updates.
- Downloading Ngspice releases.

Already-installed tools can still be detected without downloading them.

---

# 3. Project Structure

The main project structure is:

    eSim-Companion/
    │
    ├── app/
    │
    ├── config/
    │   ├── config_manager.py
    │   └── tool_paths.json
    │
    ├── services/
    │   ├── dependency_checker.py
    │   ├── tool_installer.py
    │   └── update_checker.py
    │
    ├── gui/
    │   ├── layouts/
    │   │   └── tools_layout.py
    │   └── components/
    │
    ├── docs/
    │   ├── DESIGN_DOCUMENT.md
    │   ├── EXECUTION_AND_TESTING.md
    │   └── screenshots/
    │
    ├── venv/
    │
    ├── requirements.txt
    └── README.md

The exact repository may contain additional application and utility modules.

---

# 4. Opening the Project

Open PowerShell and navigate to the project directory.

Example:

    cd C:\Users\<username>\OneDrive\Desktop\eSim-Companion

For the development environment used during testing:

    C:\Users\chitt\OneDrive\Desktop\eSim-Companion

---

# 5. Python Virtual Environment

The project uses a Python virtual environment.

## 5.1 Create a Virtual Environment

If the virtual environment does not already exist:

    python -m venv venv

## 5.2 Activate the Virtual Environment

In PowerShell:

    .\venv\Scripts\Activate.ps1

After activation, the terminal should show:

    (venv) PS C:\...\eSim-Companion>

The project commands should be executed while this environment is active.

---

# 6. Installing Python Dependencies

If the repository contains a requirements file, install the required Python packages using:

    pip install -r requirements.txt

This installs the Python libraries required by the application.

If the environment is already configured, this step does not need to be repeated.

---

# 7. Checking Python Environment

Verify the Python executable being used:

    python -c "import sys; print(sys.executable)"

Verify the Python version:

    python --version

The tested system uses:

    Python 3.12.10

The project also contains a virtual environment, but the Tool Manager intentionally detects the system Python installation used for external dependency management rather than treating the project virtual environment as the managed system Python.

---

# 8. Checking WinGet

The automated installation and update functions for Git, Python, and KiCad use Windows Package Manager.

Check whether WinGet is available:

    winget --version

The tested environment uses Windows Package Manager version:

    1.29.280

The exact WinGet version may vary depending on the Windows installation.

---

# 9. Running the Application

Start the application using the project's normal application entry point.

From the project root:

    python -m app.main

If the project uses a different entry point in the repository, use that project's configured startup module.

After successful startup, the eSim Companion graphical interface should appear.

---

# 10. Tool Manager

Open the Tool Manager from the application interface.

The Tool Manager provides:

- Automatic dependency scanning
- Installed version information
- Latest-version information
- Installation actions
- Update actions
- Executable paths
- Installation status
- Update status
- Action logging

The interface contains a Rescan button that starts a fresh dependency scan.

---

# 11. Automatic Dependency Scan

When the Tool Manager is opened, an automatic dependency scan is started.

The scan checks:

1. Python
2. Git
3. Ngspice
4. KiCad

The GUI performs the scan in a background thread so that the interface remains responsive during dependency checking.

The scan results are then displayed as individual tool cards.

---

# 12. Testing Dependency Detection

The dependency checker can also be tested directly from PowerShell.

Run:

    python -c "from services.dependency_checker import DependencyChecker; r=DependencyChecker().check_all(); print([(x.name,x.status,x.version,x.path,x.compatible) for x in r])"

The final tested result was:

    [
        ('Python', 'Installed', '3.12.10',
         'C:\\Users\\chitt\\AppData\\Local\\Programs\\Python\\Python312\\python.exe',
         True),

        ('Git', 'Installed', '2.55.0',
         'C:\\Program Files\\Git\\cmd\\git.exe',
         True),

        ('Ngspice', 'Installed', '47',
         'C:\\Users\\chitt\\Downloads\\eSim-Companion\\Ngspice\\Spice64\\bin\\ngspice_con.exe',
         True),

        ('KiCad', 'Installed', '10.0.5',
         'C:\\Program Files\\KiCad\\10.0\\bin\\kicad.exe',
         True)
    ]

This confirms that all four required tools were detected and considered compatible.

---

# 13. Testing Configuration Management

Tool paths are stored in:

    config/tool_paths.json

Display the configuration using:

    Get-Content config/tool_paths.json

The final tested configuration was:

    {
        "Python": "C:\\Users\\chitt\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
        "Git": "C:\\Program Files\\Git\\cmd\\git.exe",
        "Ngspice": "C:\\Users\\chitt\\Downloads\\eSim-Companion\\Ngspice\\Spice64\\bin\\ngspice_con.exe",
        "KiCad": "C:\\Program Files\\KiCad\\10.0\\bin\\kicad.exe"
    }

These paths are specific to the development machine and should not be copied as fixed paths on another system.

---

# 14. Testing ConfigManager

The configuration manager can be tested directly.

Run:

    python -c "from config.config_manager import ConfigManager; print(ConfigManager.load_config())"

Expected output is a dictionary containing the configured paths for the supported tools.

Individual paths can also be checked:

    python -c "from config.config_manager import ConfigManager; print('Python:', ConfigManager.get_path('Python')); print('Git:', ConfigManager.get_path('Git')); print('Ngspice:', ConfigManager.get_path('Ngspice')); print('KiCad:', ConfigManager.get_path('KiCad'))"

---

# 15. Testing Version Detection

The dependency checker extracts and normalizes installed versions.

Run:

    python -c "from services.dependency_checker import DependencyChecker; r=DependencyChecker().check_all(); print([(x.name,x.version) for x in r])"

The tested versions are:

| Tool | Installed Version |
|------|-------------------|
| Python | 3.12.10 |
| Git | 2.55.0 |
| Ngspice | 47 |
| KiCad | 10.0.5 |

---

# 16. Testing Python Version Management

The Tool Manager manages the system Python 3.12 installation.

Check the installed managed Python version:

    python -c "from services.dependency_checker import DependencyChecker; print(DependencyChecker.find_python_executable())"

The tested executable was:

    C:\Users\chitt\AppData\Local\Programs\Python\Python312\python.exe

The installed version was:

    3.12.10

The update operation was tested using:

    python -c "from services.tool_installer import ToolInstaller; print(ToolInstaller.update_python())"

The tested result was:

    Python is already up to date (version 3.12.10).

---

# 17. Testing Git Management

The Git update function can be tested using:

    python -c "from services.tool_installer import ToolInstaller; print(ToolInstaller.update_git())"

The tested result was:

    Git is already up to date (version 2.55.0).

The verified Git executable was:

    C:\Program Files\Git\cmd\git.exe

---

# 18. Testing KiCad Management

The KiCad update function can be tested using:

    python -c "from services.tool_installer import ToolInstaller; print(ToolInstaller.update_kicad())"

The tested result was:

    KiCad is already up to date (version 10.0.5).

The verified KiCad executable was:

    C:\Program Files\KiCad\10.0\bin\kicad.exe

---

# 19. Testing Ngspice Management

The Ngspice version can be checked using:

    python -c "from services.tool_installer import ToolInstaller; print('Installed:', ToolInstaller.get_installed_ngspice_version()); print('Latest:', ToolInstaller.get_latest_ngspice_version())"

The final tested result was:

    Installed: 47
    Latest: 47

The Ngspice update operation was also tested:

    python -c "from services.tool_installer import ToolInstaller; print(ToolInstaller.update_ngspice())"

The tested result indicated:

    Ngspice is already up to date (version 47).

The verified executable was:

    C:\Users\chitt\Downloads\eSim-Companion\Ngspice\Spice64\bin\ngspice_con.exe

---

# 20. Testing Invalid Path Recovery

The system was tested against an invalid saved Git executable path.

A backup of the configuration was first created.

The Git path was temporarily changed to:

    C:\invalid\git.exe

The dependency checker was then executed.

The system successfully rediscovered the actual Git installation:

    C:\Program Files\Git\cmd\git.exe

The dependency result became:

    Git
    Status: Installed
    Version: 2.55.0
    Compatible: True

The valid path was then restored to the configuration.

This confirms that the Dependency Checker can recover when a previously saved executable path is no longer valid.

---

# 21. Testing Missing Dependency Detection

A missing dependency scenario was also tested without uninstalling Git.

The saved Git configuration path was temporarily set to:

    None

The dependency checker was then tested using an intentionally invalid command:

    definitely_missing_esim_git

The result was:

    ToolResult(
        name='Git',
        installed=False,
        version=None,
        path=None,
        status='Missing',
        message='Git was not found on this system.',
        compatible=False
    )

This confirms that the system correctly identifies a dependency as missing when the executable cannot be located.

The valid Git path was restored after testing.

---

# 22. Testing WinGet Failure Handling

The system was tested with an intentionally invalid WinGet package identifier.

Command:

    python -c "from services.tool_installer import ToolInstaller; print(ToolInstaller.run_winget(['upgrade','--id','Definitely.Not.A.Real.Package.999999','-e','--silent']))"

The tested result was:

    (False, 'No installed package found matching input criteria.')

This confirms that a failed package-manager operation is returned as a failure instead of being incorrectly reported as a successful update.

---

# 23. WinGet `show` Command Handling

During development, an issue was identified with the WinGet `show` command.

The following argument was not accepted by the installed WinGet version:

    --accept-package-agreements

The system was adjusted so that package agreements are accepted for operations such as installation and upgrade, while the unsupported package-agreement argument is omitted from `show` operations.

The corrected command:

    winget show --id Python.Python.3.12 -e --source winget --accept-source-agreements

successfully returned:

    Python 3.12
    Version: 3.12.10

This confirms that the WinGet command construction is adapted to the command being executed.

---

# 24. Testing Installation Verification

Installation success is not determined solely from the return code of the package manager.

After installation, the system verifies:

1. The executable can be located.
2. The executable exists.
3. The version can be detected.
4. The installation is compatible.
5. The executable path can be saved.

The general workflow is:

    Install
       ↓
    Locate Executable
       ↓
    Verify Executable
       ↓
    Detect Version
       ↓
    Verify Version
       ↓
    Save Path
       ↓
    Report Success

If verification fails, the operation is reported as unsuccessful.

---

# 25. Testing Update Verification

Update operations follow the same verification principle.

The workflow is:

    Check Current Version
            ↓
    Determine Latest Version
            ↓
       Compare Versions
          /       \
       Same       Newer
        |           |
        ↓           ↓
    Up to Date    Update
                     ↓
                 Verify
                     ↓
              Save Verified Path
                     ↓
                Rescan Tools

For an already-current tool, the operation returns a successful result indicating that the tool is already up to date.

---

# 26. Testing GUI Action Logging

The Tool Manager records operations in the Action Log.

A typical scan produces entries such as:

    [2026-08-19 11:06:12] Starting automatic dependency scan.
    [2026-08-19 11:06:12] Scan: Python - Installed - version 3.12.10
    [2026-08-19 11:06:12] Scan: Git - Installed - version 2.55.0
    [2026-08-19 11:06:12] Scan: Ngspice - Installed - version 47
    [2026-08-19 11:06:12] Scan: KiCad - Installed - version 10.0.5

The Action Log allows the user to understand what operations the application performed.

---

# 27. GUI Testing

The Tool Manager GUI should be checked for:

- Tool cards
- Installed versions
- Installation status
- Executable paths
- Latest versions
- Update status
- Install buttons for missing tools
- Update buttons when updates are available
- Rescan button
- Action Log

The tested interface successfully displayed the detected tools and their current status.

---

# 28. Background Operation Testing

Dependency scanning and installation/update operations are executed in background threads.

This prevents long-running operations such as:

- Dependency scans
- WinGet operations
- Ngspice downloads
- Update checks

from blocking the graphical interface.

During an operation, controls such as the Rescan button are disabled where appropriate.

After the operation finishes, the interface is refreshed and dependency information is rescanned.

---

# 29. Python Syntax Testing

The main Task 5 Python modules should be checked for syntax errors.

Run:

    python -m py_compile services/tool_installer.py

Then:

    python -m py_compile services/dependency_checker.py

Then:

    python -m py_compile gui/layouts/tools_layout.py

A successful compilation produces no error output.

The Task 5 implementation was successfully compiled using these checks.

---

# 30. Complete Dependency Verification

Before final submission, run:

    python -c "from services.dependency_checker import DependencyChecker; r=DependencyChecker().check_all(); print([(x.name,x.status,x.version,x.path,x.compatible) for x in r])"

Expected final state in the tested environment:

| Tool | Status | Version | Compatible |
|------|--------|---------|------------|
| Python | Installed | 3.12.10 | True |
| Git | Installed | 2.55.0 | True |
| Ngspice | Installed | 47 | True |
| KiCad | Installed | 10.0.5 | True |

---

# 31. Final Testing Checklist

Before considering the prototype ready for submission, verify:

- [x] Python detected
- [x] Git detected
- [x] Ngspice detected
- [x] KiCad detected
- [x] Installed versions detected
- [x] Compatibility checked
- [x] Configuration loaded
- [x] Configuration saved
- [x] Invalid Git path recovery tested
- [x] Missing Git detection tested
- [x] Git update tested
- [x] Python update tested
- [x] KiCad update tested
- [x] Ngspice update tested
- [x] Invalid WinGet operation tested
- [x] GUI dependency scan tested
- [x] Action Log tested
- [x] Python syntax compilation tested
- [x] Final dependency scan verified

---

# 32. Troubleshooting

## 32.1 Virtual Environment Does Not Activate

Run:

    .\venv\Scripts\Activate.ps1

If PowerShell prevents script execution, check the local PowerShell execution policy and use an appropriate environment-specific solution rather than modifying the project code.

## 32.2 Python Command Uses the Wrong Installation

Check:

    python -c "import sys; print(sys.executable)"

Also check installed Python versions:

    py -0p

The Tool Manager is designed to identify the appropriate system Python installation rather than incorrectly treating the project virtual environment as the managed Python dependency.

## 32.3 WinGet Is Not Available

Run:

    winget --version

If the command is unavailable, the Windows Package Manager must be installed or enabled before automated Git, Python, or KiCad installation/update operations can work.

## 32.4 Dependency Is Reported as Missing

Run:

    python -c "from services.dependency_checker import DependencyChecker; r=DependencyChecker().check_all(); print([(x.name,x.status,x.version,x.path,x.compatible) for x in r])"

Check whether the executable is actually installed.

## 32.5 Configuration Contains an Invalid Path

Inspect:

    Get-Content config/tool_paths.json

The Dependency Checker should attempt to rediscover the executable if the stored path is invalid.

## 32.6 Update Operation Fails

Check:

1. Internet connection.
2. WinGet availability.
3. Package availability.
4. Tool installation state.
5. Action Log output.

The application should report the failure rather than falsely reporting a successful update.

## 32.7 Ngspice Download Fails

Check the internet connection and retry the operation.

If the official release information cannot be obtained, the application should report that it was unable to determine the latest Ngspice version.

---

# 33. Reproducibility Notes

The exact executable paths shown in this document belong to the development/test machine.

Another machine may have paths such as:

    C:\Program Files\Git\cmd\git.exe

or a different installation directory.

The application therefore uses executable discovery and persistent configuration rather than assuming that the development-machine paths exist everywhere.

Similarly, installed versions may change over time as newer releases become available.

---

# 34. Final Execution Procedure

A reviewer can reproduce the main workflow using the following sequence.

### Step 1

Open PowerShell in the project directory.

### Step 2

Activate the virtual environment:

    .\venv\Scripts\Activate.ps1

### Step 3

Install Python dependencies:

    pip install -r requirements.txt

### Step 4

Launch the application:

    python -m app.main

### Step 5

Open the Tool Manager.

### Step 6

Allow the automatic dependency scan to complete.

### Step 7

Verify Python, Git, Ngspice, and KiCad.

### Step 8

Check installed versions and latest versions in the GUI.

### Step 9

If an update is available, select Update.

### Step 10

Verify that the application confirms the updated installation.

### Step 11

Review the Action Log.

### Step 12

Run the final terminal dependency scan:

    python -c "from services.dependency_checker import DependencyChecker; r=DependencyChecker().check_all(); print([(x.name,x.status,x.version,x.path,x.compatible) for x in r])"

---

# 35. Final Result

The tested implementation successfully demonstrates:

- Automated dependency detection
- Version detection
- Compatibility checking
- Tool installation management
- Tool update management
- Ngspice release management
- Persistent configuration
- Invalid path recovery
- Missing dependency detection
- Installation/update verification
- GUI-based management
- Action logging
- Failure handling

The final tested environment reported:

    Python   → 3.12.10 → Installed → Compatible
    Git      → 2.55.0  → Installed → Compatible
    Ngspice  → 47      → Installed → Compatible
    KiCad    → 10.0.5  → Installed → Compatible

The prototype therefore provides the required execution and testing procedure for the Task 5 Automated Tool Manager.
