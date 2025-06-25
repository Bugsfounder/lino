#!/usr/bin/env python3


import sys
from PyQt5 import QtWidgets, QtGui

from manager import ClipboardManager
from gui import ClipboardUI


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Arial", 10))

    manager = ClipboardManager()
    manager.start_monitoring()

    window = ClipboardUI(manager)
    window.show()  # show directly on launch
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
