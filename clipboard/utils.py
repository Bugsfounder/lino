from PyQt5 import QtWidgets


class ClipboardManager:
    def __init__(self, max_history=20):
        self.history = []
        self.max_history = max_history
        self.clipboard = QtWidgets.QApplication.clipboard()
        self.last_content = ""

    def start_monitoring(self):
        self.clipboard.dataChanged.connect(self.on_clipboard_change)

    def on_clipboard_change(self):
        current_content = self.clipboard.text()
        if current_content and current_content != self.last_content:
            self.last_content = current_content
            self.add_to_history(current_content)

    def add_to_history(self, content):
        if content in self.history:
            self.history.remove(content)
        if not self.history or self.history[-1] != content:
            if len(self.history) >= self.max_history:
                self.history.pop(0)
            self.history.append(content)
            print(
                f"[Added] {content[:80]}..."
                if len(content) > 80
                else f"[Added] {content}"
            )
