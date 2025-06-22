from PyQt5 import QtWidgets, QtCore, QtGui


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
