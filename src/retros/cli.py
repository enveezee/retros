
import argparse
from . import core

def main():
    parser = argparse.ArgumentParser(description="RetroOS Package Manager")
    subparsers = parser.add_subparsers(dest="command")

    # 'create' command
    create_parser = subparsers.add_parser("create", help="Create a new retro package")
    create_parser.add_argument("source", help="Source directory or file for the package")
    create_parser.add_argument("-n", "--name", help="Name of the package")

    # 'install' command
    install_parser = subparsers.add_parser("install", help="Install a retro package")
    install_parser.add_argument("package", help="Path to the retro package file (e.g., my_game.squashfs)")

    # 'run' command
    run_parser = subparsers.add_parser("run", help="Run a retro package")
    run_parser.add_argument("package", help="Name of the installed package")

    # 'uninstall' command
    uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall a retro package")
    uninstall_parser.add_argument("package", help="Name of the installed package")

    args = parser.parse_args()

    if args.command == "create":
        package_path = core.create_package(args.source, args.name)
        if package_path:
            print(f"Package created at: {package_path}")
    elif args.command == "install":
        core.install_package(args.package)
    elif args.command == "run":
        core.run_package(args.package)
    elif args.command == "uninstall":
        core.uninstall_package(args.package)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
