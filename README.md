eSim Companion

Automated Tool Installation and Dependency Management

eSim Companion is a desktop application designed to simplify the detection, installation, configuration, verification, and updating of external software dependencies required by the eSim environment.

The current Tool Manager manages the following external tools:

Python

Git

Ngspice

KiCad

The application automatically detects installed tools, determines their versions, checks compatibility, identifies missing dependencies, performs supported installation and update operations, verifies installations, stores executable paths, and displays dependency information through a graphical interface.

Task Information

Internship: eSim Semester Long Internship - Autumn 2026

Task: Task 5 - Automated Tool Installation and Dependency Management

Project: eSim Companion

Author: Krishna Sai

Platform: Windows

Features

The Task 5 implementation provides the following features:

Automatic dependency detection

Installed version detection

Compatibility checking

Missing dependency detection

Automated tool installation

Automated tool updates

Executable path detection

Persistent executable path configuration

Invalid executable path recovery

Installation verification

Update verification

Graphical Tool Manager

Dependency rescanning

Action/activity logging

Error handling and failure reporting

Managed Tools

Tool

Detection

Version Check

Installation

Update

Python

Yes

Yes

Yes

Yes

Git

Yes

Yes

Yes

Yes

Ngspice

Yes

Yes

Yes

Yes

KiCad

Yes

Yes

Yes

Yes

System Architecture

The main system flow is:

                    eSim Companion
                          |
                          v
                  +---------------+
                  | Tool Manager  |
                  |      GUI      |
                  +-------+-------+
                          |
                          v
                +-------------------+
                | Dependency Checker|
                +---------+---------+
                          |
                          v
                +-------------------+
                |  Tool Installer   |
                +---------+---------+
                          |
                +---------+---------+
                |                   |
                v                   v
             WinGet              Ngspice
          Python/Git/KiCad       Download
                |                   |
                +---------+---------+
                          |
                          v
                +-------------------+
                |   Verification    |
                +---------+---------+
                          |
                          v
                +-------------------+
                |  Config Manager   |
                +---------+---------+
                          |
                          v
                +-------------------+
                | tool_paths.json   |
                +-------------------+

For the complete architecture, module responsibilities, installation workflow, update workflow, configuration management, error handling, reliability considerations, and detailed design decisions, see the Design Document.

Project Structure

eSim-Companion/
│
├── app/
│   ├── main.py
│   └── __init__.py
│
├── config/
│   ├── config_manager.py
│   ├── tools.py
│   └── tool_paths.json
│
├── services/
│   ├── dependency_checker.py
│   └── tool_installer.py
│
├── gui/
│   ├── dashboard.py
│   ├── main_window.py
│   ├── sidebar.py
│   ├── splash.py
│   ├── components/
│   ├── layouts/
│   └── pages/
│
├── docs/
│   ├── DESIGN_DOCUMENT.md
│   ├── EXECUTION_AND_TESTING.md
│   └── screenshots/
│       └── tool_manager_final.png
│
├── requirements.txt
└── README.md

The repository may contain additional supporting modules and files.

Requirements

The current implementation is primarily designed for Windows.

Required environment:

Windows 10/11

Python

Git

Windows Package Manager (WinGet)

Internet connection for installation and update operations

The project uses a Python virtual environment for development and execution.

Installation and Setup

1. Open the Project

Navigate to the project directory:

cd C:\Users\<username>\OneDrive\Desktop\eSim-Companion

Replace <username> with the Windows username on the target machine.

2. Create the Virtual Environment

If the virtual environment does not already exist:

python -m venv venv

3. Activate the Virtual Environment

In PowerShell:

.\venv\Scripts\Activate.ps1

After activation, the terminal should display something similar to:

(venv) PS C:\...\eSim-Companion>

4. Install Python Dependencies

pip install -r requirements.txt

Running the Application

The verified application entry point is:

python -m app.main

After the application starts:

Open the Tools section.

Allow the automatic dependency scan to complete.

Review the detected dependencies.

Check installed versions and status.

Use Rescan when a fresh dependency scan is required.

Use the available installation or update actions when required.

Review the Action/Activity Log for operation results.

Dependency Detection

The Dependency Checker can be tested directly from PowerShell.

Run:

python -c "from services.dependency_checker import DependencyChecker; r=DependencyChecker().check_all(); print([(x.name,x.status,x.version,x.path,x.compatible) for x in r])"

The final tested environment produced:

Python   Installed   3.12.10   True
Git      Installed   2.55.0    True
Ngspice  Installed   47        True
KiCad    Installed   10.0.5    True

This confirms that all four managed dependencies were detected and considered compatible.

Tested Environment

Tool

Tested Version

Status

Python

3.12.10

Installed / Compatible

Git

2.55.0

Installed / Compatible

Ngspice

47

Installed / Compatible

KiCad

10.0.5

Installed / Compatible

Configuration

Executable paths are stored in:

config/tool_paths.json

Example structure:

{
    "Python": "C:\\Path\\To\\python.exe",
    "Git": "C:\\Path\\To\\git.exe",
    "Ngspice": "C:\\Path\\To\\ngspice_con.exe",
    "KiCad": "C:\\Path\\To\\kicad.exe"
}

The actual paths are machine-specific and are automatically detected and stored by the application.

The configuration can be inspected using:

Get-Content config/tool_paths.json

Testing

The implementation has been tested for:

Dependency detection

Version detection

Compatibility checking

Configuration loading

Configuration saving

Invalid executable path recovery

Missing dependency detection

Git update handling

Python update handling

KiCad update handling

Ngspice update handling

WinGet failure handling

Installation verification

Update verification

GUI dependency scanning

Action logging

Python syntax compilation

Syntax Verification

The following Python modules were checked for syntax errors.

Application Entry Point

python -m py_compile app/main.py

Dependency Checker

python -m py_compile services/dependency_checker.py

Tool Installer

python -m py_compile services/tool_installer.py

Tool Manager GUI

python -m py_compile gui/layouts/tools_layout.py

A successful compilation produces no error output.

Testing Evidence

A final Tool Manager screenshot is included in:

docs/screenshots/tool_manager_final.png



The screenshot provides visual evidence of the Tool Manager interface and dependency status.

Documentation

Detailed project documentation is available in the docs directory.

Design Document

Design Document

The Design Document provides detailed information about:

Problem statement

Objectives

Scope

Functional requirements

Non-functional requirements

System architecture

Module breakdown

Dependency detection

Installation design

Update design

Configuration management

GUI design

Error handling

Reliability

Testing

Limitations

Future enhancements

Execution and Testing Instructions

Execution and Testing Instructions

This document provides detailed procedures for:

System setup

Virtual environment setup

Dependency installation

Application execution

Dependency scanning

Version checking

Configuration testing

Installation testing

Update testing

Missing dependency testing

Invalid-path recovery

Failure handling

GUI testing

Syntax testing

Troubleshooting

Final verification

Error Handling

The system handles conditions including:

Missing dependencies

Invalid executable paths

Failed WinGet operations

Download failures

Version detection failures

Installation verification failures

Update verification failures

The application does not treat a failed installation or update as successful merely because a package-manager or download operation was initiated.

Executable and version verification are performed before successful completion is reported.

Current Status

The Task 5 core implementation has been completed and tested.

Implemented functionality includes:

Automatic dependency scanning

Version detection

Compatibility checking

Tool installation management

Tool update management

Configuration persistence

Invalid path recovery

Missing dependency detection

Installation verification

Update verification

Graphical Tool Manager

Action logging

Error handling

The final verification confirmed that Python, Git, Ngspice, and KiCad were detected successfully and reported as compatible.

Limitations

The current implementation is primarily Windows-oriented.

The automated package-management implementation currently uses:

WinGet for Python

WinGet for Git

WinGet for KiCad

SourceForge release downloads for Ngspice

Linux and macOS package-manager integration is not currently implemented.

Executable paths are machine-specific and are therefore discovered and stored dynamically.

Future Enhancements

Possible future improvements include:

Linux package-manager support

macOS package-manager support

Additional dependency support

Additional package-manager integrations

Scheduled dependency checks

Improved installation progress reporting

Update rollback support

Expanded automated testing

More advanced configuration validation

Conclusion

eSim Companion provides a centralized approach to managing the external dependencies required by the eSim environment.

The Tool Manager combines:

Dependency Detection
        +
Version Management
        +
Installation
        +
Updates
        +
Verification
        +
Configuration
        +
Graphical Management
        +
Action Logging

The final tested environment successfully detected:

Python 3.12.10

Git 2.55.0

Ngspice 47

KiCad 10.0.5

All four dependencies were reported as installed and compatible during the final dependency verification.

Author

Krishna Sai

Project: eSim Companion

Task: Task 5 - Automated Tool Installation and Dependency Management