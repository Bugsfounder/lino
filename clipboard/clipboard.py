#!/usr/bin/env python3


import sys
from PyQt5 import QtWidgets, QtGui

from manager import ClipboardManager
from gui import ClipboardUI


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setStyle("Fusion")

    app.setFont(QtGui.QFont("Arial", 10))

    manager = ClipboardManager()
    manager.start_monitoring()

    window = ClipboardUI(manager)

    icon = QtGui.QIcon.fromTheme("edit-paste")
    if icon.isNull():
        icon = QtGui.QIcon(
            ":/qt-project.org/styles/commonstyle/images/dirclosed-128.png"
        )
    tray_icon = QtWidgets.QSystemTrayIcon(icon)
    tray_icon.setToolTip("Lino - Clipboard Manager")

    menu = QtWidgets.QMenu()
    show_action = QtWidgets.QAction("Show History")
    show_action.triggered.connect(window.toggle_history)
    menu.addAction(show_action)

    exit_action = QtWidgets.QAction("Exit")
    exit_action.triggered.connect(app.quit)
    menu.addAction(exit_action)

    tray_icon.setContextMenu(menu)

    tray_icon.activated.connect(
        lambda reason: (
            window.toggle_history()
            if reason == QtWidgets.QSystemTrayIcon.Trigger
            else None
        )
    )
    tray_icon.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
