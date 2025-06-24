import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QPushButton


class DropDownWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(200, 100)
        if hasattr(self, "tray") and self.tray.isVisible():
            self.tray.hide()
            self.tray.deleteLater()
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Dropdown UI Here")
        label1 = QtWidgets.QLabel("Dropdown UI Here")
        label2 = QtWidgets.QLabel("Dropdown UI Here")
        layout.addWidget(label)
        layout.addWidget(label2)
        layout.addWidget(label1)
        self.setLayout(layout)


class TrayApp(QtWidgets.QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.tray = QtWidgets.QSystemTrayIcon(QtGui.QIcon("icon.png"))
        self.tray.setToolTip("Tray App Example")
        self.dropdown = DropDownWindow()
        self.tray.activated.connect(self.on_tray_activated)
        self.tray.show()

    def on_tray_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:  # Left click
            cursor_pos = QtGui.QCursor.pos()
            w, h = self.dropdown.width(), self.dropdown.height()
            self.dropdown.move(cursor_pos.x() - w // 2, cursor_pos.y() + 10)
            self.dropdown.show()


if __name__ == "__main__":
    app = TrayApp(sys.argv)
    sys.exit(app.exec_())
