import keyboard
import pyperclip as clipboard
import time
import threading
from PyQt5 import QtWidgets
import sys

history = []
MAX_HISTORY = 20
show_gui_flag = False


class ClipboardUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipboard History")
        self.setGeometry(400, 200, 400, 300)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.itemClicked.connect(self.copy_item)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def update_history(self):
        self.list_widget.clear()
        self.list_widget.addItems(history[::-1])

    def copy_item(self, item):
        clipboard.copy(item.text())
        QtWidgets.QMessageBox.information(self, "Copied", f"Copied:\n{item.text()}")
        self.hide()


def clipboard_manager():
    global show_gui_flag
    last_clipboard_content = ""
    while True:
        try:
            if keyboard.is_pressed("ctrl") and keyboard.is_pressed("c"):
                time.sleep(0.1)
                current_content = clipboard.paste()

                if current_content and current_content != last_clipboard_content:
                    last_clipboard_content = current_content
                    if not history or history[-1] != current_content:
                        if len(history) >= MAX_HISTORY:
                            history.pop(0)
                        history.append(current_content)
                        print(f"[Copied] {current_content[:80]}")

                while keyboard.is_pressed("c") or keyboard.is_pressed("ctrl"):
                    time.sleep(0.01)

            elif (
                keyboard.is_pressed("ctrl")
                and keyboard.is_pressed("shift")
                and keyboard.is_pressed("v")
            ):
                show_gui_flag = True
                while (
                    keyboard.is_pressed("v")
                    or keyboard.is_pressed("shift")
                    or keyboard.is_pressed("ctrl")
                ):
                    time.sleep(0.01)

            time.sleep(0.05)

        except Exception as e:
            print(f"\nError: {e}")
            time.sleep(1)


def main():
    global show_gui_flag

    app = QtWidgets.QApplication(sys.argv)
    window = ClipboardUI()
    window.hide()

    # Background clipboard watcher
    threading.Thread(target=clipboard_manager, daemon=True).start()

    # Main Qt loop
    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)

    while True:
        if show_gui_flag:
            show_gui_flag = False
            window.update_history()
            window.show()
            window.raise_()
            window.activateWindow()
        app.processEvents()
        time.sleep(0.05)


if __name__ == "__main__":
    from PyQt5 import QtCore

    main()
