from PyQt5 import QtWidgets
import sys
import pyperclip


class ClipboardUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipboard History")
        self.setGeometry(300, 300, 400, 300)

        # Dummy clipboard data
        self.history = [
            "Hello, world!",
            "Copied line 1",
            "Email: user@example.com",
            "Some important text",
            "Another copy item",
        ]

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.addItems(self.history[::-1])  # Show newest on top
        self.list_widget.itemClicked.connect(self.copy_item)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def copy_item(self, item):
        pyperclip.copy(item.text())
        QtWidgets.QMessageBox.information(self, "Copied", f"Copied:\n{item.text()}")
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = ClipboardUI()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
