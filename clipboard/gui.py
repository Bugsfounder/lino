from PyQt5 import QtWidgets
import pyperclip as clipboard
from .utils import history


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
