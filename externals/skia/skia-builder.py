import subprocess as sp
import platform
import os
import re
import json
import sys
from pathlib import Path
import shutil

# For now, this builder will create a static build only for macos arm64 (Apple Silicon)

# Store root path -- starting location where this script runs
root_path = Path(".").absolute()

# Define Configuration
with open("skia-builder.config.json") as skia_builder_config_file:
    configuration = json.load(skia_builder_config_file)

# Runs a command and shows its final output live
def run(command, check=True, text=False, capture_output=False):
    # Handle Windows specific stuff
    if(platform.system() == "Windows"):
        if(shutil.which(str(command[0]) + ".exe") != None): command[0] += ".exe"
        elif(shutil.which(str(command[0]) + ".bat") != None): command[0] += ".bat"
    return sp.run([shutil.which(command[0]), *command[1:]], check=check, text=text, capture_output=capture_output)

# Set up Windows dev environment
if(platform.system() == "Windows"):
    print("Configuring Windows MSVC to target 64 bit...")

    target_arch = "x86"
    if (platform.machine() == "AMD64"):
        target_arch = "amd64"
    if (platform.machine() == "x64"):
        target_arch = "x64"
    run([str(Path(os.getenv("VCINSTALLDIR"), "Auxiliary", "Build", "vcvarsall.bat")), 
        target_arch, 
        configuration["skia"]["buildArguments"]["windows"]["win_sdk_version"]],
        f"-vcvars_ver=14.29"
        )


# Install depot_tools locally
depot_tools_path = Path("tools", "depot_tools")
if (not depot_tools_path.exists()):
    print("Installing depot_tools")
    run(["git", "clone", configuration["depot_tools"]
           ["source"]["url"], depot_tools_path])
os.environ["PATH"] = os.pathsep.join(
    [os.path.join(os.getcwd(), depot_tools_path), os.getenv("PATH")])

# Download Skia
skia_path = Path("source", "skia")
if (not skia_path.exists()):
    print("Downloading skia...")
    Path.mkdir("source")

    os.chdir("source")
    run(["fetch", "skia"])
    os.chdir(root_path)

# Compile Skia
os.chdir(skia_path)

# Checkout the defined version
run(["git", "checkout", f"chrome/{configuration['skia']['version']}"])

# Sync skia dependencies
print("Syncing Skia dependencies...")
run([sys.executable, Path("tools", "git-sync-deps")])
run([sys.executable, Path("bin", "fetch-ninja")])

# Compile / Build
skia_build_output_path = Path("out", "Release")
skia_build_arguments = configuration["skia"]["buildArguments"]
skia_build_arguments_string = ""

if(not skia_build_output_path.exists()):
    Path.mkdir(skia_build_output_path, parents=True)
with open(Path(skia_build_output_path, "args.gn"), 'w', encoding="utf-8") as file:
    for pform, args in skia_build_arguments.items():
        if (pform == "default" or 
            pform == platform.system().lower() or 
            pform == platform.machine().lower()):
            for k, v in args.items():
                processed_v = v
                if (type(v) is bool):
                    processed_v = str(v).lower()
                elif(type(v) is str):
                    processed_v = f"\"{v}\""

                    if (platform.system() == "Windows"):
                        processed_v = re.sub(r"%\w+%", 
                            lambda m: str(Path(os.getenv(m.group(0)[1:-1]))),
                            processed_v)
                file.writelines(f"{k}={processed_v}\n")

# Actually compile
print("Compiling Skia...")

run(["gn", "gen", str(skia_build_output_path), "--ide=vs"])
run(["ninja", "-C", str(skia_build_output_path)])
