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
        grid_layout = QtWidgets.QGridLayout()
        cols = 5
        for i, mod in enumerate(self.modules):
            btn = QPushButton()
            btn.setToolTip(f"{mod['name']} - {mod.get('shortcut-key', '')}")
            btn.setIcon(QtGui.QIcon(mod["icon"]))
            btn.setFixedSize(30, 30)
            btn.setIconSize(QtCore.QSize(24, 24))
            btn.setProperty("script", mod["script"])
            btn.clicked.connect(self.launch_module)
            row, col = divmod(i, cols)
            grid_layout.addWidget(btn, row, col)

        # Exit hyperlink label
        exit_label = QtWidgets.QLabel('<a href="#">Exit</a>')
        exit_label.setTextFormat(QtCore.Qt.RichText)
        exit_label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        exit_label.setOpenExternalLinks(False)
        exit_label.linkActivated.connect(QtWidgets.QApplication.quit)
        exit_label.setAlignment(QtCore.Qt.AlignRight)
        exit_label.setStyleSheet("color: #3498db; padding: 4px;")

        # Combine grid and footer
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(exit_label)
        self.setLayout(main_layout)

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
