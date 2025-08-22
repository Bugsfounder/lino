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
        self.setMinimumSize(300, 200)
        self.setup_ui()
        self.setup_shortcuts()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def setup_ui(self):
        self.setStyleSheet(
            """
            QToolTip {
                background-color: yellow;
                color: black;
                border: 1px solid black;
            }
            """
        )

        layout = QtWidgets.QGridLayout()
        layout.setVerticalSpacing(2)  # reduce gap between rows
        cols = 2

        title = QtWidgets.QLabel("Lino - Menu")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title, 0, 0, 1, cols)

        sub_title = QtWidgets.QLabel("Hover on icons to know their purpose")
        sub_title.setStyleSheet(
            "font-size: 12px; color: gray; margin-top: 2px; margin-bottom: 4px; padding:1px"
        )
        sub_title.setAlignment(QtCore.Qt.AlignCenter)
        # layout.addWidget(sub_title, 1, 0, 1, cols)

        for i, mod in enumerate(self.modules):
            btn = QtWidgets.QPushButton()
            # btn.setStyleSheet("background-color: transparent; border: none;")

            btn.setToolTip(f"{mod['name']} - {mod['shortcut-key']}")
            btn.setIcon(self.style().standardIcon(mod["icon"]))
            btn.setIconSize(QtCore.QSize(30, 30))
            btn.clicked.connect(
                lambda checked, key=mod["key"]: self.tray_app.launch_module(key)
            )
            row, col = divmod(i, cols)
            layout.addWidget(btn, row + 2, col)

        exit_label = QtWidgets.QLabel('<a href="#" style="color:gray;">Exit</a>')
        exit_label.setToolTip("Remove lino from tray")
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

    def focusOutEvent(self, event):
        self.hide()
        event.accept()
