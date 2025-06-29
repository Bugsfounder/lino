# manager/main.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt5 import QtWidgets, QtGui, QtCore
from mood.mood import DropDownWindow
from clipboard.manager import ClipboardManager
from clipboard.gui import ClipboardUI
from functools import partial
from quick_launcher.quick_launcher import QuickLauncher  # Import your QuickLauncher
from logger.logger import Logger

D_LOGGER = Logger(prod=False)
P_LOGGER = Logger(prod=True)

modules = [
    {
        "name": "Clipboard",
        "icon": "assets/icons/clipboard.png",
        "shortcut-key": "Ctrl+Shift+c",
        "key": "clipboard",
    },
    {
        "name": "Quick Launcher",
        "icon": "assets/icons/quick_launcher.png",
        "shortcut-key": "Ctrl+Space",
        "key": "quicklauncher",
    },
    # Add more modules here in the future
]


class TrayApp(QtWidgets.QApplication):
    def __init__(self, argv):
        D_LOGGER.info("Tray App Launched")
        super().__init__(argv)
        self.tray = QtWidgets.QSystemTrayIcon(QtGui.QIcon("assets/icons/clipboard.png"))
        self.dropdown = DropDownWindow(modules, self)
        self.tray.activated.connect(self.show_dropdown)
        self.tray.show()

        # Instantiate all module UIs
        self.manager = ClipboardManager()
        self.manager.start_monitoring()
        self.clipboard_ui = ClipboardUI(self.manager)
        self.quicklauncher_ui = QuickLauncher()

        # Map module keys to their UI windows
        self.module_windows = {
            "clipboard": self.clipboard_ui,
            "quicklauncher": self.quicklauncher_ui,
            # Add more as you add modules
        }

    def show_dropdown(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.dropdown.show_at_cursor()

    def launch_module(self, key):
        # Hide dropdown, show the requested module UI
        self.dropdown.hide()
        win = self.module_windows.get(key)
        if win:
            if hasattr(win, "update_history"):
                win.update_history()
            win.show()
            win.raise_()
            win.activateWindow()


def main():
    app = TrayApp(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Arial", 16))
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
