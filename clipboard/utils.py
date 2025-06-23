# clipboard/manager.py
from PyQt5.QtCore import QTimer
import pyperclip


class ClipboardManager:
    def __init__(self):
        self.history = []
        self.clipboard = pyperclip
        self.last_clip = ""
        self.MAX_HISTORY = 20

    def start_monitoring(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(300)  # check every 300 ms

    def check_clipboard(self):
        current = self.clipboard.paste()
        if current != self.last_clip and current.strip():
            self.last_clip = current
            if not self.history or self.history[-1] != current:
                if len(self.history) >= self.MAX_HISTORY:
                    self.history.pop(0)
                self.history.append(current)
                print(f"[Copied] {current[:80]}")
