# NMR5 Qt/QML validation matrix

This file records what was actually validated for the Qt/QML slice and what is
still pending on each target platform.

## Artifact types

- `package_pure`: CPack `.tar.gz` and `.zip` with the executable only. Qt must
  already be installed on the target machine.
- `package_with_qt`: platform package with Qt runtime deployment tools.
- `package_all`: runs both targets above when the platform deployment tool is
  available.

## Current status

| Platform | Build | Tests | Runtime log | `package_pure` | `package_with_qt` | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| macOS arm64, Homebrew Qt 6.11.0 | OK | OK | OK | OK | OK | Validated locally on 2026-05-08. |
| Debian | Pending | Pending | Pending | Pending | Pending | Needs distro validation with Qt packages from apt. |
| Artix | Pending | Pending | Pending | Pending | Pending | Needs distro validation with Qt packages from pacman. |
| Windows 11 | Pending | Pending | Pending | Pending | Pending | Needs validation with MSVC, Qt and `windeployqt`. |

## macOS command set

```bash
cd cpp
qt-cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
./check_runtime_log.sh
cmake --build build --target package_pure
cmake --build build --target package_with_qt
cmake --build build --target package_all
```

Validated outputs:

- `build/nmr5-qml-0.1.0-Darwin.tar.gz`
- `build/nmr5-qml-0.1.0-Darwin.zip`
- `build/deploy/nmr5-qml-0.1.0-macos-with-qt.zip`

## Debian command set

```bash
cd cpp
cmake -S . -B build -G Ninja
cmake --build build
ctest --test-dir build --output-on-failure
./check_runtime_log.sh
cmake --build build --target package_pure
```

For a Qt-bundled Linux artifact, install and validate `linuxdeployqt`, then run:

```bash
cmake --build build --target package_with_qt
```

## Artix command set

```bash
cd cpp
cmake -S . -B build -G Ninja
cmake --build build
ctest --test-dir build --output-on-failure
./check_runtime_log.sh
cmake --build build --target package_pure
```

For a Qt-bundled Linux artifact, install and validate `linuxdeployqt`, then run:

```bash
cmake --build build --target package_with_qt
```

## Windows 11 command set

Run from a Visual Studio developer shell with Qt on PATH:

```powershell
cd cpp
qt-cmake.bat -S . -B build -G Ninja
cmake --build build
ctest --test-dir build --output-on-failure
cmake --build build --target package_pure
cmake --build build --target package_with_qt
```

Run the runtime smoke through Git Bash, installed with Git for Windows:

```powershell
bash ./check_runtime_log.sh
```

The Windows Qt-bundled package uses `scripts\package_windows_qt.ps1` and
requires `windeployqt.exe` through PATH or the `WINDEPLOYQT` environment
variable.

## Release gate

Before treating a platform as release-ready, record:

- OS version and architecture.
- Qt version and install source.
- Compiler and CMake generator.
- Build, test and package command results.
- Artifact path and size.
- Runtime smoke result from either `check_runtime_log.sh` or a platform-specific
  equivalent.
