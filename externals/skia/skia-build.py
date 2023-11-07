import subprocess as sp
import platform
import os
import json
from textwrap import dedent
from pathlib import Path

# For now, this builder will create a static build only for macos arm64 (Apple Silicon)

# Store root path -- starting location where this script runs
root_path = Path(".").absolute()

# Define Configuration
with open("skia-build.config.json") as skia_builder_config_file:
    configuration = json.load(skia_builder_config_file)

# Install depot_tools locally
depot_tools_path = Path("tools", "depot_tools")
if(not depot_tools_path.exists()):
    print("Installing depot_tools")
    sp.run(["git", "clone", configuration["depot_tools"]["source"]["url"], depot_tools_path], check=True)
os.environ["PATH"] = os.pathsep.join([os.path.join(os.getcwd(), depot_tools_path), os.getenv("PATH")])

# Download Skia
skia_path = Path("source", "skia")
if(not skia_path.exists()):
    print("Downloading skia...")
    Path.mkdir("source")

    os.chdir("source")
    sp.run(["fetch", "skia"], check=True)
    os.chdir(root_path)

# Compile Skia
os.chdir(skia_path)
skia_gn_path = Path("bin", "gn")
skia_ninja_path = Path("bin", "ninja")

## Checkout the defined version
sp.run(["git", "checkout", f"chrome/{configuration['skia']['version']}"], check=True)

## Sync skia dependencies
print("Syncing Skia dependencies...")
sp.run(["python3", Path("tools", "git-sync-deps")], check=True)
sp.run([Path("bin", "fetch-ninja")], check=True)

## Compile / Build
skia_build_arguments=dedent("""
is_official_build=true 
cc="clang" 
cxx="clang++" 
skia_use_system_expat=false 
skia_use_system_harfbuzz=false
skia_use_system_libpng=false 
skia_use_system_libjpeg_turbo=false 
skia_use_system_libwebp=false 
skia_use_system_icu=false 
skia_use_system_zlib=false
""")

### Configuring for ARM
if platform.machine() == "arm64":
    skia_build_arguments+=dedent("""
    target_cpu="arm64" 
    """).strip()

### Configuration for Apple
if platform.system() == "Darwin":
    skia_build_arguments+=dedent("""
    target_os="mac"
    """).strip()

### Actually compile
print("Compiling Skia...")
skia_build_output_path=Path("out", "StaticAppleSilicon")
sp.run([skia_gn_path, "gen", skia_build_output_path, f"--args={skia_build_arguments}"], check=True)
sp.run([skia_ninja_path, "-C", skia_build_output_path], check=True)
