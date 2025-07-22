
# RetroOS Package Manager Design

This document outlines the broader vision and design principles for the RetroOS package manager, `retros`.

## 1. Core Philosophy

The `retros` package manager aims to simplify the management and execution of retro software (games, applications, emulators) on a modern Linux system. It prioritizes:

*   **Simplicity:** Easy for users to install and run retro content without deep technical knowledge.
*   **Portability:** Packages should be self-contained and work across different RetroOS installations and potentially other Linux distributions.
*   **Reproducibility:** Ensure that a package, once created, can be reliably installed and run in the future, regardless of system changes.
*   **Isolation:** Retro software should run in an isolated environment to prevent conflicts with the host system.
*   **Extensibility:** Easy to add support for new emulators, game formats, and retro applications.

## 2. Package Specification

### 2.1. Retro Package Format (SquashFS Image)

Retro packages will be distributed as SquashFS (`.squashfs`) images. This format provides:

*   **Read-only:** Ensures package integrity and prevents accidental modification.
*   **Compressed:** Reduces storage footprint.
*   **Self-contained:** All necessary files (game data, metadata, potentially emulator configurations) are bundled within the image.
*   **Mountable:** Can be mounted as a filesystem, allowing direct access to its contents without extraction.

**Important Note:** `.squashfs` images are *not* the distributable format for retro content due to copyright considerations. They are created locally from legally obtained original game files.

### 2.2. `metadata.json`

Each `.squashfs` package will contain a `metadata.json` file at its root. This file will be the central source of truth for package information and execution instructions. Key fields include:

*   `name` (string): Display name of the package.
*   `version` (string): Version of the retro content.
*   `description` (string): A brief description of the package.
*   `emulator` (string): The name of the emulator required (e.g., "dosbox", "mame", "scummvm").
*   `emulator_path` (string): Absolute path to the emulator executable on the host system (e.g., "/usr/bin/dosbox"). This will be a suggestion, and the system will verify its existence.
*   `emulator_args` (array of strings): Command-line arguments to pass to the emulator.
*   `game_path_in_package` (string): Path to the main game executable or data file *within the mounted SquashFS image* (e.g., "DOOM.EXE", "game/start.sh").
*   `original_source_name` (string): The name of the original source directory/file used to create the package. Useful for internal tracking and path construction.
*   `dependencies` (array of strings): List of system-level package dependencies (e.g., "dosbox", "mame", "libsdl2-2.0-0"). These are packages that `retros` will attempt to install via the system's package manager.
*   `run_command` (string, optional): A custom command to execute if the standard `emulator`/`game_path_in_package` logic is insufficient. This would override the default execution flow.

## 3. User Experience (CLI & Future GUI)

### 3.1. CLI (`retros` command)

The command-line interface will provide essential functionalities:

*   `retros create <source_archive> --name <package_name>`: Creates a new `.squashfs` package.
    *   This command will internally utilize the `jetson` project to detect the archive type (RAR, ZIP, ISO, etc.), extract its contents, and then package the extracted data along with `metadata.json` into a `.squashfs` image.
*   `retros install <package_file>`: Installs the `.squashfs` image and registers it as an installed game within Lutris. This will involve:
    *   Checking for and offering to install system dependencies.
    *   Copying the `.squashfs` file to a designated installation directory.
    *   Generating Lutris configuration files that point to the `.squashfs` file and provide Lutris with the game's metadata (emulator, arguments, etc.).
*   `retros run <package_name>`: Launches an installed game by instructing Lutris to execute it. This provides a seamless "Start Menu" like experience, bypassing the Lutris GUI if desired.
*   `retros uninstall <package_name>`: Unregisters the game from Lutris and removes the `.squashfs` file.
*   `retros list`: Lists all installed retro packages (registered with Lutris).
*   `retros info <package_name>`: Displays detailed information about an installed package (retrieved from Lutris's configuration or the `.squashfs`'s internal metadata).

### 3.2. Future GUI

The GUI will provide a more intuitive and visually appealing experience, especially for non-technical users. Key features:

*   **Package Browser:** A visual list of available and installed packages, with search and filter capabilities.
*   **Installation Wizard:** A guided process for installing new packages, including dependency resolution and progress indicators.
*   **Launch Pad:** Easy access to launch installed games/applications with customizable settings.
*   **Settings:** Configuration options for `retros` itself (e.g., default install directory, emulator paths).
*   **Retro-themed Aesthetics:** The GUI should align with the overall RetroOS theme, potentially mimicking classic operating system interfaces or game launchers.

## 4. Installation & Run Process

### 4.1. Installation Flow

1.  User initiates `retros install <package_file.squashfs>`.
2.  `retros` reads the `metadata.json` from the `.squashfs` file (potentially by temporarily mounting it).
3.  `retros` checks for system dependencies listed in `metadata.json`.
4.  If dependencies are missing, `retros` prompts the user to install them (using `sudo` and the appropriate system package manager, e.g., `apt-get`).
5.  `retros` copies the `<package_file.squashfs>` to a designated installation directory (e.g., `/opt/retro_packages/`).
6.  `retros` generates Lutris configuration files (e.g., `.json` or `.yml`) for the game, pointing to the installed `.squashfs` file and incorporating metadata like emulator, arguments, and game path within the mounted image.
7.  `retros` registers this configuration with Lutris, making the game available in Lutris's library.
8.  The package is now considered "installed" and ready to run via Lutris.

### 4.2. Run Flow

1.  User initiates `retros run <package_name>` (e.g., from a custom RetroOS launcher or the CLI).
2.  `retros` translates this request into a Lutris launch command (e.g., `lutris lutris://rungame/<game_id>`).
3.  Lutris executes the game. Lutris's runner will be configured to mount the `.squashfs` file using `squashfuse` to a temporary mount point.
4.  Lutris then launches the specified emulator with the correct arguments, pointing to the game files within the temporary mount point.
5.  Upon game exit, Lutris's runner automatically unmounts the SquashFS image.

## 5. Integration with RetroOS

`retros` will be a core component of RetroOS. It will be pre-installed and integrated into the system's user interface. The RetroOS environment will provide:

*   **Pre-configured Emulators:** Common emulators will be pre-installed and their paths configured within `retros`.
*   **System-level Mount Points:** Standardized locations for mounted retro packages.
*   **Boot-time Mounting (Optional):** For frequently used packages, `retros` could offer an option to automatically mount them at boot.

## 6. Future Considerations

*   **Package Updates:** A mechanism for updating installed packages.
*   **Version Management:** Support for multiple versions of the same package.
*   **Online Repository:** A centralized repository for discovering and downloading retro packages.
*   **Save Game Management:** Tools for backing up and restoring save game data.
*   **Controller Configuration:** Integration with controller mapping tools.
*   **Web Integration:** As discussed, a retro web browser that leverages `retros` for content delivery.
