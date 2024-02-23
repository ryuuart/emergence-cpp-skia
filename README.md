# Emergence CPP Skia

Quick starting point for those who want to use Skia and C++. I am providing build scripts because it was very painful to build this manually.

## Getting Started

### Requirements

- Python 3

### Configuring the Skia builder

Build is currently for developers. Skia will have debug symbols and more included. TODO: allow more unified configuration between CMake and skia-builder.

In `externals/skia/skia-builder.config.json`, you should manually configure what you need. Particularly on Windows, you should configure `clang_win` to your CLang installation.

Most of these are Google GN arguments. You can find out about them by running, `bin/gn args out/Debug --list` from the Skia source folder. If you need Google's Depot Tools, it'll be in the `externals/skia/tools/depot_tools` folder. You can do this after you've [downloaded Skia](#downloading-and-building-skia).

### Downloading and building Skia

**This will download all of Skia, its dependencies, and build tools** then compile/build it as a library. Right now, it's built as a static library. If you're on Windows, make sure you have your development environment [properly configured](#requirements-for-windows).

Now, `cd` to `externals/skia`

```shell
python3 skia-builder.py
```

## Building the test app

Make sure you're in the root folder with `CMakeLists.txt` and `CMakePresets.json`

### MacOS

```shell
cmake --preset local-ninja-arm64-macos-clang
cmake --build --preset local-ninja-arm64-macos-clang-release
```

### Windows

```shell
cmake --preset local-ninja-arm64-windows-clang
cmake --build --preset local-ninja-arm64-windows-clang-release
```

## Requirements for Windows

This skia build currently uses the static CRT.

- **Make sure Visual Studio 2019 or 2022 is installed with C++ (MSVC) and Windows SDK (version 10.0.20348.0)**. It should be automatically checked if you chose the C++ Desktop Environment setup during installation. You'll have to manually add the Windows SDK version because it's a specific version.
- Make sure to run _anything on the command line_ in the [Visual Studio developer shell](https://learn.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=msvc-170)
- ~~You must download a separate copy of [LLVM CLang](https://clang.llvm.org/). **Do not use the optional Clang packages / components from Visual Studio**~~ The default LLVM clang-cl (16.0.5) installed with Visual Studio should work now.
- You're gonna have to make sure [longpaths are enabled](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry) because paths get long. Setting longpaths on windows may require a registry edit, but I couldn't get Skia to be compiled without it being enabled.
- You can theoretically use the [Build Tools for Visual Studio](https://visualstudio.microsoft.com/downloads/?q=build+tools+for+visual+studio) but it hasn't been tested

> **Pro-tip**
>
> You can install LLVM-CLang on Windows with `winget` using `winget install LLVM.LLVM`.

## License

[MIT License](/LICENSE)
