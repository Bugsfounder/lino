# manager/mood/mood.py
from PyQt5 import QtWidgets, QtGui, QtCore


class DropDownWindow(QtWidgets.QWidget):
    def __init__(self, modules, tray_app):
        super().__init__()
        self.modules = modules
        self.tray_app = tray_app
        self.setWindowFlags(QtCore.Qt.Popup)
        self.setFixedSize(300, 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QGridLayout()
        cols = 2
        for i, mod in enumerate(self.modules):
            btn = QtWidgets.QPushButton()
            btn.setText(mod["name"])
            btn.setIcon(QtGui.QIcon(mod["icon"]))
            btn.setIconSize(QtCore.QSize(24, 24))
            btn.clicked.connect(
                lambda checked, key=mod["key"]: self.tray_app.launch_module(key)
            )
            row, col = divmod(i, cols)
            layout.addWidget(btn, row, col)
        self.setLayout(layout)

    def show_at_cursor(self):
        cursor_pos = QtGui.QCursor.pos()
        w, h = self.width(), self.height()
        self.move(cursor_pos.x() - w // 2, cursor_pos.y() + 10)
        self.show()
