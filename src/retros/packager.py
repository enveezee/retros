
import os
import json
import tempfile
import shutil
import subprocess

def create_self_mounting_executable(source_dir, package_name, metadata=None):
    """Creates a self-mounting executable from a source directory.
    This involves creating a SquashFS image and embedding it into a bash script.
    Returns the absolute path to the created executable.
    """
    print(f"Creating self-mounting executable for '{package_name}' from {source_dir}")

    # Define the output filename for the executable
    executable_filename = f"{package_name}.run"

    with tempfile.TemporaryDirectory() as temp_staging_dir:
        # 1. Create the SquashFS image
        squashfs_image_path = os.path.join(temp_staging_dir, f"{package_name}.squashfs")
        
        # Copy source content to staging directory for mksquashfs
        source_basename = os.path.basename(source_dir)
        destination_path = os.path.join(temp_staging_dir, source_basename)
        if os.path.isdir(source_dir):
            shutil.copytree(source_dir, destination_path)
        else:
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            shutil.copy(source_dir, destination_path)

        # Create metadata.json directly in the staged content
        metadata_path = os.path.join(destination_path, "metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata or {}, f)

        print(f"Running mksquashfs on {temp_staging_dir} to {squashfs_image_path}")
        try:
            subprocess.run(["mksquashfs", temp_staging_dir, squashfs_image_path, "-no-progress"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error creating SquashFS image: {e}")
            return None

        # 2. Read the executable template
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir, "executable_template.sh")
        with open(template_path, "r") as f:
            template_content = f.read()

        # 3. Get SquashFS image size
        squashfs_size = os.path.getsize(squashfs_image_path)

        # 4. Replace placeholders in the template
        # The offset will be the size of the template content itself
        # We'll write the template content first, then append the squashfs image
        # So, the offset is effectively the size of the template content + any newlines/etc.
        # For simplicity, we'll calculate it after writing the template to a temp file
        
        # Create a temporary file for the script part to calculate its size
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_script_file:
            # Replace placeholders that don't depend on offset yet
            script_content = template_content.replace("$PACKAGE_NAME$", package_name)
            script_content = script_content.replace("$SQUASHFS_SIZE$", str(squashfs_size))
            temp_script_file.write(script_content)
        
        # Calculate the offset (size of the script part)
        squashfs_offset = os.path.getsize(temp_script_file.name)
        os.unlink(temp_script_file.name) # Clean up the temporary script file

        # Now replace the offset placeholder in the actual script content
        script_content = script_content.replace("$SQUASHFS_OFFSET$", str(squashfs_offset))

        # 5. Concatenate the modified template and the SquashFS image
        with open(executable_filename, "wb") as out_file:
            out_file.write(script_content.encode('utf-8'))
            with open(squashfs_image_path, "rb") as in_file:
                out_file.write(in_file.read())

        # 6. Make the new file executable
        os.chmod(executable_filename, 0o755)
    
    print(f"Self-mounting executable created successfully at {os.path.abspath(executable_filename)}")
    return os.path.abspath(executable_filename)
