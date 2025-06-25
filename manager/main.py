from mood.mood import DropDownWindow
from PyQt5 import QtWidgets, QtGui
import sys

modules = [
    {
        "name": "Clipboard",
        "script": "clipboard/clipboard.py",
        "icon": "assets/icons/icon.png",
    },
    {
        "name": "Quick Launcher",
        "script": "quick_launcher/quick_launcher.py",
        "icon": "assets/icons/icon.png",
    },
]


class TrayApp(QtWidgets.QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.tray = QtWidgets.QSystemTrayIcon(QtGui.QIcon("icons/clipboard.png"))
        self.dropdown = DropDownWindow(modules)
        self.tray.activated.connect(self.show_dropdown)
        self.tray.show()

    def show_dropdown(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            cursor_pos = QtGui.QCursor.pos()
            w, h = self.dropdown.width(), self.dropdown.height()
            self.dropdown.move(cursor_pos.x() - w // 2, cursor_pos.y() + 10)
            self.dropdown.show()


if __name__ == "__main__":
    app = TrayApp(sys.argv)
    sys.exit(app.exec_())
