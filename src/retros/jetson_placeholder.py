import os
import json
import tempfile
import shutil
import subprocess
import re

def create_squashfs_image(source_dir, package_name, metadata=None):
    """Creates a SquashFS image from a source directory, including metadata.json.
    Returns the absolute path to the created SquashFS image.
    """
    print(f"Creating SquashFS image for '{package_name}' from {source_dir}")

    # Define the output filename for the executable
    squashfs_output_path = os.path.join(os.getcwd(), f"{package_name}.squashfs") # Create in current working directory for now

    with tempfile.TemporaryDirectory() as staging_dir:
        # Copy source content to staging directory for mksquashfs
        source_basename = os.path.basename(source_dir)
        destination_path = os.path.join(staging_dir, source_basename)
        if os.path.isdir(source_dir):
            shutil.copytree(source_dir, destination_path)
        else:
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            shutil.copy(source_dir, destination_path)

        # Create metadata.json directly in the staged content
        metadata_path = os.path.join(destination_path, "metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata or {}, f)

        print(f"Running mksquashfs on {staging_dir} to {squashfs_output_path}")
        try:
            mksquashfs_result = subprocess.run(["mksquashfs", staging_dir, squashfs_output_path, "-no-progress", "-noappend"], capture_output=True, text=True, check=True)
            print("mksquashfs stdout:")
            print(mksquashfs_result.stdout)
            print("mksquashfs stderr:")
            print(mksquashfs_result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Error creating SquashFS image: {e}")
            print("mksquashfs stdout:")
            print(e.stdout)
            print("mksquashfs stderr:")
            print(e.stderr)
            return None

        # Verify the created SquashFS image
        try:
            file_check_result = subprocess.run(["file", squashfs_output_path], capture_output=True, text=True, check=True)
            print("File command output for SquashFS image:")
            print(file_check_result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error verifying SquashFS image with 'file' command: {e}")
            return None
    
    print(f"SquashFS image created successfully at {os.path.abspath(squashfs_output_path)}")
    return os.path.abspath(squashfs_output_path)