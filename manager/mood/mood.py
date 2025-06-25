import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QPushButton
import subprocess
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut


class DropDownWindow(QtWidgets.QWidget):
    def __init__(self, modules):
        super().__init__()
        self.modules = modules
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(300, 200)
        self.setup_ui()
        self.setup_shortcuts()

    def setup_ui(self):
        layout = QtWidgets.QGridLayout()
        cols = 5
        for i, mod in enumerate(self.modules):
            btn = QPushButton()
            btn.setToolTip(f"{mod["name"]} - {mod['shortcut-key']}")
            # btn.setStyleSheet(
            #     """
            #         background-color: #3498db;
            #         color: white;
            #         font-weight: bold;
            #         border: 5px solid red;

            #         border-radius: 8px;
            #         padding: 6px;
            #     }
            #     """
            # )
            # btn.setStyleSheet("QPushButton { cursor: pointer; }")
            btn.setIcon(QtGui.QIcon(mod["icon"]))
            btn.setFixedSize(30, 30)
            btn.setIconSize(QtCore.QSize(24, 24))
            btn.setProperty("script", mod["script"])
            btn.clicked.connect(self.launch_module)
            row, col = divmod(i, cols)
            layout.addWidget(btn, row, col)
        self.setLayout(layout)

    def setup_shortcuts(self):
        for mod in self.modules:
            shortcut_key = mod.get("shortcut-key")
            if shortcut_key:
                shortcut = QShortcut(QKeySequence(shortcut_key), self)
                # Use lambda default arg to capture script path
                shortcut.activated.connect(
                    lambda s=mod["script"]: self.launch_script(s)
                )

    def launch_module(self):
        script = self.sender().property("script")
        self.launch_script(script)

    def launch_script(self, script):
        subprocess.Popen(["python3", script])
        self.hide()
