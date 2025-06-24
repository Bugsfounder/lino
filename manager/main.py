from PyQt5 import QtWidgets, QtGui
import sys

from clipboard.manager import ClipboardManager
from clipboard.gui import ClipboardUI
from quick_launcher.quick_launcher import QuickLauncher


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Arial", 10))

    # Clipboard part
    manager = ClipboardManager()
    manager.start_monitoring()
    clipboard_window = ClipboardUI(manager)

    icon = QtGui.QIcon.fromTheme("edit-paste")
    if icon.isNull():
        icon = QtGui.QIcon(
            ":/qt-project.org/styles/commonstyle/images/dirclosed-128.png"
        )
    tray_icon = QtWidgets.QSystemTrayIcon(icon)
    tray_icon.setToolTip("Lino - Clipboard Manager")

    menu = QtWidgets.QMenu()
    show_action = QtWidgets.QAction("Show History")
    show_action.triggered.connect(clipboard_window.toggle_history)
    menu.addAction(show_action)

    exit_action = QtWidgets.QAction("Exit")
    exit_action.triggered.connect(app.quit)
    menu.addAction(exit_action)

    tray_icon.setContextMenu(menu)

    tray_icon.activated.connect(
        lambda reason: (
            clipboard_window.toggle_history()
            if reason == QtWidgets.QSystemTrayIcon.Trigger
            else None
        )
    )
    tray_icon.show()

    # Quick Launcher part
    launcher_window = QuickLauncher()
    launcher_window.hide()  # start hidden, show on demand

    from PyQt5.QtWidgets import QShortcut
    from PyQt5.QtGui import QKeySequence
    from PyQt5.QtCore import Qt

    # inside your main() after creating launcher_window:

    shortcut = QShortcut(QKeySequence("Ctrl+Space"), clipboard_window)
    shortcut.activated.connect(
        lambda: launcher_window.setVisible(not launcher_window.isVisible())
    )

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
