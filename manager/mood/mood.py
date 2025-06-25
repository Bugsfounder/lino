import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QPushButton
import subprocess


class DropDownWindow(QtWidgets.QWidget):
    def __init__(self, modules):
        super().__init__()
        self.modules = modules
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(300, 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QGridLayout()
        cols = 5
        for i, mod in enumerate(self.modules):
            btn = QPushButton()
            btn.setToolTip(mod["name"])
            btn.setIcon(QtGui.QIcon(mod["icon"]))
            btn.setIconSize(QtCore.QSize(24, 24))
            btn.setProperty("script", mod["script"])
            btn.clicked.connect(self.launch_module)
            row, col = divmod(i, cols)
            layout.addWidget(btn, row, col)
        self.setLayout(layout)

    def launch_module(self):
        script = self.sender().property("script")
        subprocess.Popen(["python3", script])
        self.hide()
