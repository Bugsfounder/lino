from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import subprocess


class PopupUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 300, 300, 200)

        # Frameless, always on top
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.Tool
            | QtCore.Qt.WindowStaysOnTopHint
        )
        self.setWindowOpacity(0.96)

        self.hide_timer = QtCore.QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)

        self.init_theme()
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Clipboard 1"))
        layout.addWidget(QtWidgets.QLabel("Clipboard 2"))
        self.setLayout(layout)

    def init_theme(self):
        if is_dark_mode():
            self.setStyleSheet("background-color: #2e2e2e; color: white;")
        else:
            self.setStyleSheet("background-color: white; color: black;")

    def showEvent(self, event):
        self.activateWindow()
        self.setFocus()
        self.hide_timer.start(5000)

    def focusOutEvent(self, event):
        self.hide()


def is_dark_mode():
    try:
        output = (
            subprocess.check_output(
                ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"]
            )
            .decode()
            .strip()
        )
        return "dark" in output.lower()
    except Exception:
        return False  # default to light if error


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = PopupUI()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
