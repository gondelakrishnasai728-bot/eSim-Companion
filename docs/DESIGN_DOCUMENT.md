# eSim Companion
## Automated Tool Installation and Dependency Management System

### Task 5 - Design Document

**Internship:** eSim Semester Long Internship - Autumn 2026
**Task:** Task 5 - Tool Manager
**Project:** eSim Companion
**Author:** Krishna Sai
---

# 1. Introduction

## 1.1 Project Overview

eSim Companion is a desktop application designed to simplify the installation, configuration, verification, and maintenance of external software dependencies required by the eSim environment.

The application manages the following external tools:

- Python
- Git
- Ngspice
- KiCad

Instead of requiring users to manually locate installers, configure executable paths, check installed versions, and repeatedly search for updates, eSim Companion provides a centralized Tool Manager.

The system automatically detects installed dependencies, determines their versions, checks compatibility, identifies available updates, performs supported installation and update operations, verifies the resulting installation, and stores executable paths for future use.

The overall process follows:

    Detect
       ↓
    Check
       ↓
    Install / Update
       ↓
    Verify
       ↓
    Configure
       ↓
    Rescan
       ↓
    Report

---

# 2. Problem Statement

Setting up and maintaining the external tools required by an eSim environment can involve several manual operations.

Users may need to:

1. Find the correct software package.
2. Download and install the software.
3. Determine where the executable was installed.
4. Configure the executable path.
5. Check whether the installed version is compatible.
6. Periodically check whether a newer version is available.
7. Update the software manually.
8. Reconfigure the application when an executable path changes.

These manual activities can result in incorrect paths, outdated dependencies, incompatible versions, and unnecessary user effort.

eSim Companion addresses these problems by providing automated dependency detection, installation management, update management, configuration handling, and verification through a graphical Tool Manager.

---

# 3. Objectives

The main objectives of the Task 5 implementation are:

1. Detect required external tools automatically.
2. Identify installed versions.
3. Check compatibility with required versions.
4. Detect missing dependencies.
5. Install supported dependencies automatically.
6. Check for newer versions.
7. Update supported dependencies.
8. Verify installations after installation or update.
9. Automatically locate executable files.
10. Store executable paths persistently.
11. Recover from invalid stored executable paths.
12. Provide a graphical interface for dependency management.
13. Display tool status and update information.
14. Maintain an action log for tool-management operations.
15. Reduce manual dependency-management effort.

---

# 4. Scope

The current implementation manages four major external dependencies:

| Tool | Detection | Version Check | Installation | Update |
|------|-----------|---------------|--------------|--------|
| Python | Yes | Yes | Yes | Yes |
| Git | Yes | Yes | Yes | Yes |
| Ngspice | Yes | Yes | Yes | Yes |
| KiCad | Yes | Yes | Yes | Yes |

The current implementation is primarily designed for Windows.

The package-management mechanisms currently used are:

- Windows WinGet for Git
- Windows WinGet for Python
- Windows WinGet for KiCad
- SourceForge release download for Ngspice

Cross-platform package-manager support is not currently implemented.

---

# 5. Functional Requirements

## 5.1 Automatic Tool Detection

The system shall detect whether required external tools are installed.

## 5.2 Version Detection

The system shall determine the installed version of each detected tool.

## 5.3 Compatibility Checking

The system shall determine whether an installed version satisfies the configured compatibility requirement.

For example:

    Required Python version: 3.12.0
    Installed Python version: 3.12.10

Since:

    3.12.10 >= 3.12.0

the installation is considered compatible.

## 5.4 Installation Management

The system shall provide automated installation for supported tools.

## 5.5 Update Management

The system shall determine whether a newer version is available and perform supported update operations.

## 5.6 Configuration Management

The system shall store executable paths so that they can be reused during future application executions.

## 5.7 Verification

Installation and update operations shall be verified before being reported as successful.

## 5.8 User Interface

The system shall provide a graphical Tool Manager through which users can view dependency status and perform supported actions.

---

# 6. Non-Functional Requirements

## 6.1 Reliability

The application should not report an installation or update as successful when the resulting executable cannot be verified.

## 6.2 Maintainability

The dependency-management functionality is divided into separate modules so that individual components can be modified without redesigning the entire system.

## 6.3 Usability

Users should be able to manage dependencies without manually searching for executable locations.

## 6.4 Persistence

Detected executable paths should remain available after the application is restarted.

## 6.5 Error Handling

Failures such as missing executables, invalid paths, failed package-manager operations, and download failures should be handled without unnecessarily destroying valid configuration.

---

# 7. System Architecture

The system follows a modular architecture in which the GUI communicates with the dependency-management services.

## 7.1 High-Level Architecture

    ┌──────────────────────────────────┐
    │          eSim Companion          │
    │              GUI                 │
    │          Tool Manager            │
    └────────────────┬─────────────────┘
                     │
                     ▼
    ┌──────────────────────────────────┐
    │       Dependency Checker         │
    │                                  │
    │  • Detect tools                  │
    │  • Locate executables            │
    │  • Detect versions               │
    │  • Check compatibility           │
    │  • Detect missing tools          │
    └────────────────┬─────────────────┘
                     │
                     ▼
    ┌──────────────────────────────────┐
    │          Tool Installer          │
    │                                  │
    │  • Install tools                 │
    │  • Update tools                  │
    │  • Verify installations          │
    │  • Download Ngspice              │
    └──────────────┬─────────┬─────────┘
                   │         │
          ┌────────┘         └─────────────┐
          ▼                                ▼
    ┌──────────────┐                ┌──────────────┐
    │    WinGet    │                │   Ngspice    │
    │              │                │ SourceForge  │
    │ Python       │                │ Download     │
    │ Git          │                │ Extraction   │
    │ KiCad        │                └──────────────┘
    └──────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │        Configuration Manager     │
    │                                  │
    │  • Load configuration            │
    │  • Save configuration            │
    │  • Read tool paths               │
    │  • Update tool paths             │
    └────────────────┬─────────────────┘
                     │
                     ▼
    ┌──────────────────────────────────┐
    │          tool_paths.json         │
    └──────────────────────────────────┘

---

# 8. Module Breakdown

## 8.1 Dependency Checker

### Purpose

The Dependency Checker is responsible for detecting and validating external dependencies.

### Main responsibilities

- Detect installed tools.
- Locate executable files.
- Determine installed versions.
- Check compatibility.
- Detect missing dependencies.
- Detect invalid saved paths.
- Rediscover tools when stored paths become invalid.
- Return structured dependency results.

### Processing Flow

    Tool Definition
          ↓
    Read Saved Path
          ↓
    Is Path Valid?
       /        \
     Yes         No
      |           |
      |       Search PATH /
      |       Known Locations
      |           |
      └─────┬─────┘
            ↓
      Locate Executable
            ↓
      Run Version Command
            ↓
       Extract Version
            ↓
     Check Compatibility
            ↓
       Return Result

### Tool Result

The dependency checker produces a structured result containing information such as:

- Tool name
- Installation state
- Version
- Executable path
- Status
- Message
- Compatibility state

---

# 9. Tool Installer

## 9.1 Purpose

The Tool Installer performs automated installation and update operations.

### Responsibilities

- Execute package-manager operations.
- Install supported tools.
- Update supported tools.
- Download Ngspice releases.
- Extract Ngspice archives.
- Locate executables.
- Verify executable availability.
- Verify versions.
- Save verified executable paths.

---

# 10. Tool Definitions

Tool information is maintained separately so that the dependency-management system can use consistent metadata for each supported tool.

A tool definition contains information such as:

- Tool name
- Display name
- Command
- Version arguments
- Minimum supported version

For example:

    Python
        Command: python
        Version argument: --version
        Minimum version: 3.12.0

    Git
        Command: git
        Version argument: --version
        Minimum version: 2.40.0

Ngspice and KiCad are also represented in the tool configuration, with their version requirements handled according to the current implementation.

---

# 11. Tool Installation Design

## 11.1 WinGet Installation

Git, Python, and KiCad use Windows WinGet for automated installation.

The workflow is:

    User selects Install
            ↓
    Identify Tool
            ↓
    Identify WinGet Package
            ↓
    Execute Installation
            ↓
    Check Command Result
            ↓
    Locate Executable
            ↓
    Verify Executable
            ↓
    Verify Version
            ↓
    Save Path
            ↓
    Refresh Dependency Status
            ↓
    Display Result

## 11.2 Ngspice Installation

Ngspice follows a download-based installation workflow.

    Request Ngspice Installation
              ↓
    Determine Release
              ↓
    Obtain Download URL
              ↓
    Download Archive
              ↓
    Extract Archive
              ↓
    Locate ngspice_con.exe
              ↓
    Verify Executable
              ↓
    Verify Version
              ↓
    Save Path
              ↓
    Refresh Dependency Status

---

# 12. Update and Upgrade Design

The update system compares the installed version with the latest available version.

## 12.1 Update Flow

    Installed Version
            ↓
    Latest Available Version
            ↓
      Compare Versions
          /       \
        Same      Newer
         |          |
         ▼          ▼
     Up to Date   Update
                    ↓
                 Verify
                    ↓
              Save Path
                    ↓
              Refresh GUI

## 12.2 Already Up-to-Date

If the installed version is already the latest version, no unnecessary update is performed.

For example:

    Installed Git: 2.55.0
    Latest Git:    2.55.0

Result:

    Git is already up to date.

## 12.3 Update Verification

After an update, the application verifies the executable and installed version before reporting success.

---

# 13. Dependency Checking

The Dependency Checker performs an automatic scan of the supported tools.

The general process is:

    Start Dependency Scan
            ↓
    Check Python
            ↓
    Check Git
            ↓
    Check Ngspice
            ↓
    Check KiCad
            ↓
    Collect Results
            ↓
    Display Results in GUI

The tested environment produced:

    Python   Installed   3.12.10
    Git      Installed   2.55.0
    Ngspice  Installed   47
    KiCad    Installed   10.0.5

All four were detected as compatible.

---

# 14. Missing Dependency Handling

If an executable cannot be located, the dependency checker reports the dependency as missing.

Example:

    Executable Not Found
            ↓
    Status = Missing
            ↓
    User Can Initiate Installation

The system does not assume that a dependency exists simply because its name is present in the configuration.

---

# 15. Invalid Path Recovery

The system supports recovery when a stored executable path becomes invalid.

The process is:

    Saved Executable Path
            ↓
       Path Valid?
        /       \
      Yes        No
       |          |
       |      Search System
       |      PATH / Known
       |       Locations
       |          ↓
       |      Find Executable
       |          ↓
       └──────┬───┘
              ↓
        Verify Executable
              ↓
        Verify Version
              ↓
         Save New Path

This behavior was tested using an intentionally invalid Git path.

The system successfully rediscovered Git and restored the valid executable location.

---

# 16. Configuration Management

## 16.1 ConfigManager

The Configuration Manager provides persistent configuration storage.

Its responsibilities include:

- Loading saved configuration.
- Saving configuration.
- Getting a tool path.
- Setting a tool path.
- Creating default configuration when required.

## 16.2 Configuration File

The configuration is stored in:

    config/tool_paths.json

The current tested configuration contains:

    Python → Python312\python.exe
    Git → Git\cmd\git.exe
    Ngspice → Spice64\bin\ngspice_con.exe
    KiCad → 10.0\bin\kicad.exe

The exact paths are machine-specific.

---

# 17. Interaction Between Modules

The main interaction between components is:

    Tool Manager GUI
            ↓
    Dependency Checker
            ↓
    Tool Installer
            ↓
    Installation / Update
            ↓
    Verification
            ↓
    Config Manager
            ↓
    tool_paths.json
            ↓
    Dependency Checker
            ↓
    Updated GUI

This interaction ensures that changes made by installation or update operations are reflected in the dependency status displayed to the user.

---

# 18. User Interface Design

## 18.1 Sidebar Design

The application uses a fixed-width navigation sidebar placed on the left side of the window.

The sidebar is data-driven, generating navigation buttons from a predefined list rather than hardcoding each button individually.

This improves maintainability and allows future navigation items to be added with minimal code changes.

Current navigation items:

- Dashboard
- Scanner
- Tools
- Configure
- Updates
- Activity

## 18.2 Tool Manager

The Tools section provides the main interface for dependency management.

The interface displays information such as:

- Tool name
- Installed version
- Latest version
- Installation state
- Update state
- Available actions

## 18.3 Activity / Action Log

The application records tool-management operations through the Activity or Action Log area.

This provides visibility into:

- Dependency scans
- Installation operations
- Update operations
- Successful operations
- Failed operations

---

# 19. GUI Interaction Flow

    Application Starts
            ↓
    Tool Manager Loads
            ↓
    Automatic Dependency Scan
            ↓
    Tool Status Displayed
            ↓
    User Selects Action
            ↓
    Installer / Updater
            ↓
    Verification
            ↓
    Configuration Update
            ↓
    Dependency Rescan
            ↓
    GUI Refresh
            ↓
    Action Log Updated

---

# 20. Error Handling

The system handles several failure conditions.

## 20.1 Missing Dependency

    Executable Not Found
            ↓
    Status = Missing
            ↓
    User Can Install

## 20.2 Invalid Path

    Stored Path Invalid
            ↓
    Search for Executable
            ↓
    Rediscover Tool
            ↓
    Update Configuration

## 20.3 Package Manager Failure

    Package Operation
            ↓
        Failure
            ↓
      Return False
            ↓
    Report Failure
            ↓
    Preserve Valid Configuration

## 20.4 Download Failure

If an Ngspice download fails, the operation is reported as unsuccessful rather than being treated as a completed installation.

## 20.5 Verification Failure

If installation completes but the resulting executable cannot be verified, the system reports the operation as failed.

---

# 21. Reliability Design

The system uses multiple verification stages.

### Executable Verification

The expected executable must be located.

### Version Verification

The application obtains the actual installed version.

### Compatibility Verification

The detected version is compared with the configured requirements.

### Configuration Protection

Failed operations should not unnecessarily replace valid stored paths.

### Recovery

Invalid stored paths can be rediscovered.

---

# 22. Testing and Validation

The implementation was tested using normal operation, failure simulation, and recovery scenarios.

| Test Case | Expected Result | Result |
|-----------|-----------------|--------|
| Python detection | Python detected | Passed |
| Git detection | Git detected | Passed |
| Ngspice detection | Ngspice detected | Passed |
| KiCad detection | KiCad detected | Passed |
| Python version detection | 3.12.10 | Passed |
| Git version detection | 2.55.0 | Passed |
| Ngspice version detection | 47 | Passed |
| KiCad version detection | 10.0.5 | Passed |
| Configuration loading | Paths loaded | Passed |
| Invalid Git path | Git rediscovered | Passed |
| Missing Git simulation | Missing status | Passed |
| Git update | Verified | Passed |
| Python update | Verified | Passed |
| KiCad update | Verified | Passed |
| Ngspice update | Verified | Passed |
| Invalid WinGet operation | Failure returned | Passed |
| GUI dependency scan | All tools displayed | Passed |

---

# 23. Final Tested Environment

The final dependency scan successfully detected:

| Tool | Version | Status | Compatible |
|------|---------|--------|------------|
| Python | 3.12.10 | Installed | Yes |
| Git | 2.55.0 | Installed | Yes |
| Ngspice | 47 | Installed | Yes |
| KiCad | 10.0.5 | Installed | Yes |

---

# 24. Security and Reliability Considerations

The implementation uses defined package and download mechanisms.

For WinGet-managed tools, package identifiers are explicitly configured.

For Ngspice, the application obtains the configured release archive and verifies the resulting executable.

The system does not consider an operation successful solely because a download or package-manager command completed. Executable and version verification are performed before final success is reported.

---

# 25. Limitations

The current implementation has the following limitations:

1. The automated installation/update implementation is primarily Windows-oriented.
2. Git, Python, and KiCad package management depends on WinGet.
3. Ngspice depends on the configured release download source.
4. Stored executable paths are machine-specific.
5. Linux and macOS package-manager integration is not currently implemented.

Cross-platform support can be considered as a future enhancement.

---

# 26. Future Enhancements

Possible future improvements include:

1. Linux package-manager support.
2. macOS package-manager support.
3. Additional dependency support.
4. Additional package-manager integrations.
5. Scheduled dependency checks.
6. Improved installation progress reporting.
7. Update rollback support.
8. Expanded automated testing.
9. More advanced configuration validation.
10. Additional recovery mechanisms.

---

# 27. Conclusion

eSim Companion provides a centralized and automated approach to managing the external dependencies required by the eSim environment.

The implemented system combines:

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
    Graphical Interface
            +
    Action Logging

The modular architecture separates dependency checking, installation and update operations, configuration management, and user-interface functionality.

Testing confirmed successful detection of Python, Git, Ngspice, and KiCad, version identification, configuration persistence, invalid-path recovery, missing-dependency detection, update verification, failure handling, and GUI operation.

The implementation therefore provides the required foundation for automated tool installation and dependency management in eSim Companion.