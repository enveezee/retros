from .package import RetroPackage
from . import jetson_placeholder as packager
import os
import subprocess
import tempfile
import shutil
import json

def create_package(source, name):
    """Creates a new retro package."""
    package = RetroPackage(name)
    # Example metadata
    metadata = {
        "name": name,
        "version": "1.0",
        "description": f"A retro package for {name}",
        "emulator": "dosbox", # Placeholder
        "emulator_path": "/usr/bin/dosbox", # Example path
        "emulator_args": [], # Example arguments
        "game_path_in_package": "game.txt", # Path to the game executable/file within the package
        "run_command": "game.exe", # Placeholder
        "original_source_name": os.path.basename(source),
        "dependencies": ["dosbox"] # List of system package dependencies
    }
    return packager.create_squashfs_image(source, f"{name}.squashfs", metadata)

def check_dependencies(dependencies):
    """Checks if the given system dependencies are installed."""
    # TODO: Implement a more robust dependency check for different Linux distributions (apt, yum, dnf, pacman)
    return []

def install_dependencies(dependencies):
    """Installs the given system dependencies using apt-get."""
    print("Dependency installation is currently a placeholder. Please install dependencies manually if needed.")
    return True

def install_package(package_path):
    """Installs a retro package."""
    package_name = os.path.basename(package_path).replace(".squashfs", "")
    install_dir = "/home/nvz/Documents/gemini-cli/retros/gemini_workspace/installed_packages"
    package = RetroPackage(package_name)

    # Temporarily mount the SquashFS image to read metadata
    temp_mount_point = os.path.join(tempfile.gettempdir(), f"temp_mount_{package_name}")
    os.makedirs(temp_mount_point, exist_ok=True)
    try:
        subprocess.run(["squashfuse", "-o", "nonempty", package_path, temp_mount_point], check=True)
        metadata_path = os.path.join(temp_mount_point, "metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
            dependencies = metadata.get("dependencies", [])
            if dependencies:
                missing_deps = check_dependencies(dependencies)
                if missing_deps:
                    print(f"Missing dependencies: {missing_deps}")
                    if install_dependencies(missing_deps):
                        print("Dependencies installed. Proceeding with package installation.")
                    else:
                        print("Failed to install dependencies. Aborting package installation.")
                        return
        else:
            print(f"Warning: metadata.json not found in {package_path}. Cannot check dependencies.")
    except subprocess.CalledProcessError as e:
        print(f"Error temporarily mounting SquashFS image to check metadata: {e}")
        return
    finally:
        if os.path.ismount(temp_mount_point):
            subprocess.run(["fusermount", "-u", temp_mount_point], check=True)
        if os.path.exists(temp_mount_point):
            shutil.rmtree(temp_mount_point)

    # Copy the .squashfs file to the installed_packages directory
    installed_squashfs_path = os.path.join(install_dir, os.path.basename(package_path))
    os.makedirs(install_dir, exist_ok=True)
    shutil.copy(package_path, installed_squashfs_path)
    print(f"Package copied to {installed_squashfs_path}")

    # TODO: Generate Lutris configuration and register it
    print("TODO: Generate Lutris configuration and register it.")


def run_package(package_name):
    """Runs an installed retro package via Lutris."""
    print(f"Attempting to run {package_name} via Lutris...")
    try:
        # Assuming Lutris game ID is the same as package_name for now
        subprocess.run(["lutris", f"lutris://rungame/{package_name}"], check=True)
        print(f"Successfully launched {package_name} via Lutris.")
    except FileNotFoundError:
        print("Error: Lutris not found. Please ensure Lutris is installed and in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error launching {package_name} via Lutris: {e}")

def uninstall_package(package_name):
    """Uninstalls a retro package."""
    install_dir = "/home/nvz/Documents/gemini-cli/retros/gemini_workspace/installed_packages"
    installed_squashfs_path = os.path.join(install_dir, f"{package_name}.squashfs")

    # TODO: Unregister from Lutris
    print(f"TODO: Unregister {package_name} from Lutris.")

    if os.path.exists(installed_squashfs_path):
        os.remove(installed_squashfs_path)
        print(f"Removed package file: {installed_squashfs_path}")
    else:
        print(f"Warning: Package file not found at {installed_squashfs_path}")
