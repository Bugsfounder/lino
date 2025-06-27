from PyQt5 import QtWidgets, QtGui, QtCore


class ClipboardUI(QtWidgets.QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.itemClicked.connect(self.copy_item)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

        clear_btn = QtWidgets.QPushButton("Clear History")
        clear_btn.clicked.connect(self.clear_history)
        # clear_btn.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(clear_btn)

    def update_history(self):
        self.list_widget.clear()
        self.list_widget.addItems(self.manager.history[::-1])

    def copy_item(self, item):
        self.manager.clipboard.setText(item.text())
        QtWidgets.QToolTip.showText(
            QtGui.QCursor.pos(), "Copied to clipboard!", self, QtCore.QRect(), 2000
        )
        self.hide()

    def clear_history(self):
        self.manager.history.clear()
        self.list_widget.clear()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.hide()

    def clear_history(self):
        self.manager.history.clear()
        self.update_history()
