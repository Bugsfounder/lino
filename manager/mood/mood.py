# manager/mood/mood.py
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence


class DropDownWindow(QtWidgets.QWidget):
    def __init__(self, modules, tray_app):
        super().__init__()
        self.modules = modules
        self.tray_app = tray_app
        self.setWindowFlags(QtCore.Qt.Popup)
        # self.setFixedSize(300, 200)
        self.setMinimumSize(300, 200)
        self.setup_ui()
        self.setup_shortcuts()

    def setup_ui(self):
        layout = QtWidgets.QGridLayout()
        cols = 2
        for i, mod in enumerate(self.modules):
            btn = QtWidgets.QPushButton()
            btn.setToolTip(f"{mod["name"]} - {mod['shortcut-key']}")
            # btn.setText(mod["name"])
            btn.setIcon(QtGui.QIcon(mod["icon"]))
            btn.setIconSize(QtCore.QSize(24, 24))
            btn.clicked.connect(
                lambda checked, key=mod["key"]: self.tray_app.launch_module(key)
            )
            row, col = divmod(i, cols)
            layout.addWidget(btn, row, col)

        # Add Exit link at bottom
        exit_label = QtWidgets.QLabel('<a href="#">Exit</a>')
        exit_label.setStyleSheet("color: blue; text-decoration: underline;")
        exit_label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        exit_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        exit_label.linkActivated.connect(QtWidgets.qApp.quit)

        layout.addWidget(
            exit_label, layout.rowCount(), 0, 1, cols, alignment=QtCore.Qt.AlignCenter
        )
        self.setLayout(layout)

    def setup_shortcuts(self):
        for mod in self.modules:
            shortcut_key = mod.get("shortcut-key")
            if shortcut_key:
                shortcut = QShortcut(QKeySequence(shortcut_key), self)
                shortcut.activated.connect(
                    lambda key=mod["key"]: self.tray_app.launch_module(key)
                )

    def show_at_cursor(self):
        cursor_pos = QtGui.QCursor.pos()
        w, h = self.width(), self.height()
        self.move(cursor_pos.x() - w // 2, cursor_pos.y() + 10)
        self.show()
