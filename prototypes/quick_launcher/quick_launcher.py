# quick_launcher.py

import sys
import subprocess
from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QApplication,
    QListWidget,
    QListWidgetItem,
)
from PyQt5.QtCore import Qt
import re


# def is_expression(text):
#     return re.fullmatch(r"[0-9+\-*/%.() ]+", text) is not None


class QuickLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lino Quick Launcher")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(600, 300, 400, 50)
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        x = (rect.width() - self.width()) // 2
        y = (rect.height() - self.height()) // 2
        self.move(x, y)

        self.input = QLineEdit(self)
        self.input.setGeometry(10, 10, 380, 30)
        self.input.setPlaceholderText("Type to launch... (e.g., firefox)")
        self.input.returnPressed.connect(self.launch_command)
        self.input.setFocus()

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(10, 45, 380, 100)
        self.list_widget.hide()
        # self.input.textChanged.connect(self.update_dropdown)

        # self.list_widget.itemClicked.connect(self.item_selected)

    def is_expression(text):
        return text.startswith("=") and re.fullmatch(r"=[0-9+\-*/%.() ]+", text)

    def launch_command(self):
        cmd = self.input.text().strip()

        if not cmd:
            return

        if cmd.startswith("="):
            expr = cmd[1:].strip()  # remove '='
            try:
                result = eval(expr)
                self.input.setText(str(result))
            except Exception:
                self.input.setText("Invalid Expression")
        else:
            try:
                subprocess.Popen([cmd])
                self.hide()
                self.input.clear()
            except Exception:
                self.input.setText("Command Failed")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
            self.input.clear()

    # def item_selected(self, item):
    #     self.input.setText(item.text())
    #     self.launch_command()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = QuickLauncher()
    launcher.show()
    sys.exit(app.exec_())
