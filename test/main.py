#!/usr/bin/env python3

import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: lino [clipboard|quicklauncher]")
        sys.exit(1)

    module = sys.argv[1].lower()

    if module == "clipboard":
        from clipboard.clipboard import main as clipboard_main

        clipboard_main()
    elif module == "quicklauncher":
        from quick_launcher.quick_launcher import main as quick_launcher_main

        quick_launcher_main()
    else:
        print(f"Unknown module: {module}")
        sys.exit(1)


if __name__ == "__main__":
    main()
