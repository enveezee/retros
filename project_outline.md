# RetroOS Project Outline

This document breaks down the development of RetroOS into manageable tasks.

## Phase 1: Core Package Manager ("retros") - **(In Progress)**

1.  **Package Format Definition:**
    *   Defined the structure of the read-only image format for retro packages using **SquashFS (.squashfs)**.
    *   Implemented a `metadata.json` file at the root of the SquashFS image to store package information (name, version, description, emulator, emulator_path, emulator_args, game_path_in_package, original_source_name, dependencies).

2.  **Package Creation Tool:**
    *   Developed a command-line tool (`retros create`) to create retro packages from a source directory.
    *   Implemented logic to extract and pack files into the defined image format, with the SquashFS image creation logic refactored into `retros/packager.py` (which will eventually be part of the `jetson` project).

3.  **Package Installation and Execution:**
    *   Implemented the `retros install` command to copy the `.squashfs` package to a designated installation directory and initiate registration with Lutris (Lutris integration is a placeholder).
    *   Implemented the `retros uninstall` command to remove the `.squashfs` package and initiate unregistration from Lutris (Lutris integration is a placeholder).
    *   Implemented the `retros run` command to launch an installed game by instructing Lutris to execute it (Lutris integration is a placeholder).

## Phase 2: System Integration

1.  **Dependency Management:**
    *   (Planned) Integrate the "retros" package manager with the underlying OS package manager (e.g., apt, pacman) to handle dependencies. This will involve replacing the current placeholder functions with actual system calls to check and install dependencies.

2.  **User Interface:**
    *   (Planned) Design and develop a user-friendly interface for browsing, installing, and launching retro packages. This will be a graphical user interface (GUI).

## Phase 3: Retro Experience

1.  **Retro TV (Fieldstation42 Integration):**
    *   (Planned) Integrate Fieldstation42 to provide a seamless retro TV experience.
    *   (Planned) Develop a channel guide and other UI elements.

2.  **Retro Web Browser:**
    *   (Planned) Create a custom web browser that renders modern websites with a retro look and feel.
    *   (Planned) Utilize a headless browser engine (e.g., Selenium) to handle modern web technologies.

## Phase 4: Distribution

1.  **Live CD/Installable Image:**
    *   (Planned) Create a bootable ISO image of the RetroOS distribution.
    *   (Planned) Develop an installer to allow users to install RetroOS on their systems.

2.  **Package for Other Distributions:**
    *   (Planned) Package the "retros" tools for installation on other Linux distributions.