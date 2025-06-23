from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QApplication,
    QListWidget,
    QListWidgetItem,
)
from PyQt5.QtCore import Qt
import subprocess
import re, sys

import webbrowser

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

from datetime import datetime


class QuickLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.bot = ChatBot("LinoBot", read_only=True)
        # trainer = ChatterBotCorpusTrainer(self.bot)
        # trainer.train("chatterbot.corpus.english")

        self.setWindowTitle("Lino Quick Launcher")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(600, 300, 400, 150)  # increase height for dropdown

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

        # Dummy app list for prototype (replace with real apps later)
        self.apps = [
            "firefox",
            "code",
            "terminal",
            "calculator",
            "gedit",
            "nautilus",
            "first",
            "second",
        ]

    def is_expression(self, text):
        return text.startswith("=") and re.fullmatch(r"=[0-9+\-*/%.() ]+", text)

    def launch_command(self):
        cmd = self.input.text().strip()

        if not cmd:
            return

        if self.is_expression(cmd):
            expr = cmd[1:].strip()
            try:
                result = eval(expr)
                self.input.setText(str(result))
            except Exception:
                self.input.setText("Invalid Expression")
        elif cmd.startswith("http") or ".com" in cmd or ".org" in cmd:
            webbrowser.open(cmd if cmd.startswith("http") else "https://" + cmd)
            self.hide()
            self.input.clear()
            return
        elif cmd.startswith("?"):
            query = cmd[1:].strip().lower()

            if "time" in query:
                now = datetime.now().strftime("%I:%M %p")
                self.input.setText(f"Current time is {now}")
                return

            elif "date" in query:
                today = datetime.now().strftime("%A, %d %B %Y")
                self.input.setText(f"Today is {today}")
                return
            elif "your name" in query:
                self.input.setText("I'm Lino — your Linux assistant 🚀")
                return

            elif "joke" in query:
                self.input.setText(
                    "Why don't scientists trust atoms? Because they make up everything!"
                )
                return
            else:
                try:
                    response = str(self.bot.get_response(query))
                    # self.input.setText(response)
                    self.list_widget.clear()
                    QListWidgetItem(str(response), self.list_widget)
                    self.list_widget.show()
                    # self.list_widget.hide()
                except Exception:
                    self.input.setText("Sorry, I didn't get that.")
            return

        else:
            try:
                subprocess.Popen([cmd])
                self.hide()
                self.input.clear()
                self.list_widget.hide()
            except Exception:
                self.input.setText("Command Failed")

    def update_dropdown(self, text):
        if not text or text.startswith("="):
            self.list_widget.hide()
            return

        matches = [app for app in self.apps if text.lower() in app.lower()]
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
        elif event.key() == Qt.Key_Down:
            if self.list_widget.isVisible():
                self.list_widget.setFocus()
                self.list_widget.setCurrentRow(0)
        else:
            super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if obj == self.list_widget and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                current_item = self.list_widget.currentItem()
                if current_item:
                    self.input.setText(current_item.text())
                    self.launch_command()
                    return True
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = QuickLauncher()
    launcher.show()
    sys.exit(app.exec_())
