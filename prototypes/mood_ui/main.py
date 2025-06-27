import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QPushButton


class DropDownWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        # self.setFixedSize(300, 200)
        self.setMinimumSize(300, 200)

        layout = QtWidgets.QGridLayout()

        # Generate buttons dynamically
        count = 0
        total = 15  # for m1 to m15, you can change to n
        cols = 5  # 5 buttons per row

        for i in range(total):
            btn = QPushButton(f"m{i+1}")
            btn.setProperty("value", f"value-{i+1}")
            btn.setFixedSize(50, 50)
            btn.clicked.connect(lambda _, x=i + 1: self.on_button_click(x))
            row = i // cols
            col = i % cols
            layout.addWidget(btn, row, col)

        self.setLayout(layout)

    def on_button_click(self, index):
        btn = self.sender()
        val = btn.property("value")

        print(f"Button m{index} clicked value {val}")
        self.hide()


class TrayApp(QtWidgets.QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        # self.tray = QtWidgets.QSystemTrayIcon(QtGui.QIcon("icon.png"))
        self.tray = QtWidgets.QSystemTrayIcon(QtGui.QIcon("/assets/lino.png"))
        self.tray.setToolTip("hello from lino")
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
