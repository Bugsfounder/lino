from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QApplication,
    QListWidget,
    QListWidgetItem,
    QLabel,
)
from PyQt5.QtCore import Qt
import subprocess
import webbrowser
from chatterbot import ChatBot
from datetime import datetime
import sys


class QuickLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.bot = ChatBot("LinoBot", read_only=True)

        self.setWindowTitle("Lino Quick Launcher")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(600, 300, 400, 180)  # increased height

        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        x = (rect.width() - self.width()) // 2
        y = (rect.height() - self.height()) // 2
        self.move(x, y)

        self.input = QLineEdit(self)
        self.input.setGeometry(10, 10, 380, 30)
        self.input.setPlaceholderText("Type to launch... (e.g., firefox)")
        self.input.returnPressed.connect(self.launch_command)
        self.input.textChanged.connect(self.update_dropdown)
        self.input.setFocus()

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(10, 45, 380, 100)
        self.list_widget.hide()
        self.list_widget.itemClicked.connect(self.item_selected)
        self.list_widget.installEventFilter(self)

        self.ai_response = QLabel(self)
        self.ai_response.setGeometry(10, 45, 380, 120)
        self.ai_response.setWordWrap(True)
        self.ai_response.setStyleSheet(
            "background-color: #fff; color: #000; padding: 5px; border: 1px solid #ccc;"
        )
        self.ai_response.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.ai_response.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.ai_response.hide()

    def launch_command(self):
        cmd = self.input.text().strip()
        if not cmd:
            return

        self.ai_response.hide()

        if cmd.startswith("="):
            try:
                result = eval(cmd[1:].strip())
                self.input.setText(str(result))
            except:
                self.input.setText("Invalid Expression")
            return

        elif cmd.startswith("?"):
            query = cmd[1:].strip().lower()
            try:
                response = str(self.bot.get_response(query))
                self.ai_response.setText(response)
                self.ai_response.show()
                self.ai_response.raise_()
                self.ai_response.repaint()
            except:
                self.ai_response.setText("Sorry, I didn't get that.")
                self.ai_response.show()
            return

        elif cmd.startswith("http") or ".com" in cmd or ".org" in cmd:
            webbrowser.open(cmd if cmd.startswith("http") else "https://" + cmd)
            self.hide()
            self.input.clear()
            return

        else:
            try:
                subprocess.Popen([cmd])
                self.hide()
                self.input.clear()
                self.list_widget.hide()

            except:
                self.input.setText("Command Failed")
            self.input.setFocus()

    def update_dropdown(self, text):
        self.ai_response.hide()

        if not text or text.startswith("=") or text.startswith("?"):
            self.list_widget.hide()
            return

        matches = [
            app
            for app in [
                "firefox",
                "code",
                "terminal",
                "calculator",
                "gedit",
                "nautilus",
            ]
            if text.lower() in app.lower()
        ]
        self.list_widget.clear()

        if matches:
            for app in matches:
                QListWidgetItem(app, self.list_widget)
            self.list_widget.show()
        else:
            self.list_widget.hide()

    def item_selected(self, item):
        self.input.setText(item.text())
        self.launch_command()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
            self.input.clear()
            self.list_widget.hide()
            self.ai_response.hide()

        elif event.key() == Qt.Key_Down:
            if self.list_widget.isVisible():
                self.list_widget.setFocus()
                self.list_widget.setCurrentRow(0)

        else:
            super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if obj == self.list_widget and event.type() == event.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                current_item = self.list_widget.currentItem()
                if current_item:
                    self.input.setText(current_item.text())
                    self.launch_command()
                    return True

            elif event.key() == Qt.Key_Up:
                current_row = self.list_widget.currentRow()
                if current_row > 0:
                    self.list_widget.setCurrentRow(current_row - 1)
                return True

            elif event.key() == Qt.Key_Down:
                current_row = self.list_widget.currentRow()
                if current_row < self.list_widget.count() - 1:
                    self.list_widget.setCurrentRow(current_row + 1)
                return True

        return super().eventFilter(obj, event)


def main():
    app = QApplication(sys.argv)
    launcher = QuickLauncher()
    launcher.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = QuickLauncher()
    launcher.show()
    sys.exit(app.exec_())
