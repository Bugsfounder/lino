import sys
from PyQt5 import QtWidgets, QtCore, QtGui


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
        if not self.history or self.history[-1] != content:
            if len(self.history) >= self.max_history:
                self.history.pop(0)
            self.history.append(content)
            print(
                f"[Copied] {content[:80]}..."
                if len(content) > 80
                else f"[Copied] {content}"
            )


class ClipboardUI(QtWidgets.QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.setWindowTitle("Clipboard History")
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
        )
        self.setGeometry(400, 200, 500, 400)

        self.setup_ui()
        self.hide()

    def setup_ui(self):
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.itemClicked.connect(self.copy_item)

        self.search_box = QtWidgets.QLineEdit()
        self.search_box.setPlaceholderText("Search history...")
        self.search_box.textChanged.connect(self.filter_history)

        self.clear_button = QtWidgets.QPushButton("Clear History")
        self.clear_button.clicked.connect(self.clear_history)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.search_box)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.clear_button)
        self.setLayout(layout)

    def toggle_history(self):
        if self.isVisible():
            self.hide()
        else:
            self.update_history()
            self.show()
            self.raise_()
            self.activateWindow()

    def filter_history(self):
        search_text = self.search_box.text().lower()
        self.list_widget.clear()
        filtered = [
            item
            for item in reversed(self.manager.history)
            if search_text in item.lower()
        ]
        self.list_widget.addItems(filtered)

    def update_history(self):
        self.list_widget.clear()
        self.list_widget.addItems(reversed(self.manager.history))

    def clear_history(self):
        self.manager.history.clear()
        self.list_widget.clear()

    def copy_item(self, item):
        self.manager.clipboard.setText(item.text())
        QtWidgets.QToolTip.showText(
            QtGui.QCursor.pos(), "Copied to clipboard!", self, QtCore.QRect(), 2000
        )
        self.hide()

    def closeEvent(self, event):
        event.ignore()
        self.hide()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setStyle("Fusion")

    font = QtGui.QFont("Arial", 10)
    app.setFont(font)

    manager = ClipboardManager()
    manager.start_monitoring()
    window = ClipboardUI(manager)

    # Tray icon
    # tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon.fromTheme("edit-paste"))

    icon = QtGui.QIcon.fromTheme("edit-paste")
    if icon.isNull():
        icon = QtGui.QIcon(
            ":/qt-project.org/styles/commonstyle/images/dirclosed-128.png"
        )
    tray_icon = QtWidgets.QSystemTrayIcon(icon)

    tray_icon.setToolTip("Lino - Clipboard Manager")

    # ✅ Tray icon menu
    menu = QtWidgets.QMenu()
    menu = QtWidgets.QMenu()
    show_action = QtWidgets.QAction("Show History")
    show_action.triggered.connect(window.toggle_history)
    menu.addAction(show_action)

    exit_action = QtWidgets.QAction("Exit")
    exit_action.triggered.connect(app.quit)
    menu.addAction(exit_action)

    tray_icon.setContextMenu(menu)

    def tray_activated(reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            window.toggle_history()

    tray_icon.activated.connect(tray_activated)
    tray_icon.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
