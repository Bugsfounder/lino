import threading
from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QApplication,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
import subprocess
import webbrowser
import sys
import os
import glob


class SearchWorker(QObject):
    results_ready = pyqtSignal(list)

    def __init__(self, query, root, max_depth=4):
        super().__init__()
        self.query = query
        self.root = root
        self.user_uid = os.getuid()
        self.max_depth = max_depth

    def run(self):
        results = []
        root_depth = self.root.rstrip(os.sep).count(os.sep)
        for dirpath, dirnames, filenames in os.walk(self.root):
            # Limit search depth
            current_depth = dirpath.rstrip(os.sep).count(os.sep) - root_depth
            if current_depth >= self.max_depth:
                dirnames[:] = []
            # Filter out root-owned directories in-place
            dirnames[:] = [
                d for d in dirnames if self._is_owned_by_user(os.path.join(dirpath, d))
            ]
            for name in dirnames:
                if self.query.lower() in name.lower():
                    results.append((name, os.path.join(dirpath, name), "folder"))
                    if len(results) >= 50:  # Limit for performance
                        self.results_ready.emit(results)
                        return
            for name in filenames:
                full_path = os.path.join(dirpath, name)
                if not self._is_owned_by_user(full_path):
                    continue
                if self.query.lower() in name.lower():
                    results.append((name, full_path, "file"))
                    if len(results) >= 50:
                        self.results_ready.emit(results)
                        return
        self.results_ready.emit(results)

    def _is_owned_by_user(self, path):
        try:
            return os.stat(path).st_uid == self.user_uid
        except Exception:
            return False


class QuickLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lino Quick Launcher")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setMinimumSize(400, 200)  # Allow resizing, but not too small

        # Set dark palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(40, 40, 40))
        dark_palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(60, 120, 200))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        QApplication.instance().setPalette(dark_palette)

        # Set font
        font = QFont("Arial", 9)
        QApplication.instance().setFont(font)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Type to launch... (e.g., firefox)")
        self.input.returnPressed.connect(self.launch_command)
        self.input.textChanged.connect(self.on_text_changed)
        self.input.setFont(font)
        self.input.setStyleSheet(
            """
            QLineEdit {
                background: #222;
                color: #fff;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
            }
        """
        )
        layout.addWidget(self.input, stretch=0)

        self.list_widget = QListWidget(self)
        self.list_widget.setFont(font)
        self.list_widget.setStyleSheet(
            """
            QListWidget {
                background: #181818;
                color: #eee;
                border: 1px solid #444;
                border-radius: 6px;
                font-size: 12px;
            }
            QListWidget::item:selected {
                background: #3a6ea5;
                color: #fff;
            }
            QScrollBar:vertical {
                background: #222;
                width: 10px;
                margin: 2px 0 2px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #444;
                min-height: 20px;
                border-radius: 5px;
            }
        """
        )
        self.list_widget.itemClicked.connect(self.item_selected)
        self.list_widget.installEventFilter(self)
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_widget.setMinimumHeight(340)
        self.list_widget.setMaximumHeight(340)
        layout.addWidget(self.list_widget, stretch=1)

        self.setLayout(layout)

        # Show the window first to get its size
        self.show()
        frame_geom = self.frameGeometry()
        screen = QApplication.primaryScreen()
        center_point = screen.availableGeometry().center()
        frame_geom.moveCenter(center_point)
        self.move(frame_geom.topLeft())

        # Caching and paging
        self.apps_cache = self.get_installed_apps()
        self.fs_results = []
        self.fs_query = ""
        self.fs_thread = None
        self.fs_worker = None
        self.page = 0
        self.page_size = 5

        # Debounce timer for search
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._do_search)

        self._drag_active = False
        self._drag_position = None

    def launch_command(self):
        cmd = self.input.text().strip()

        if cmd.startswith("="):
            try:
                result = eval(cmd[1:].strip())
                self.input.blockSignals(True)
                self.input.setText(str(result))
                self.input.blockSignals(False)
            except:
                self.input.blockSignals(True)
                self.input.setText("Invalid Expression")
                self.input.blockSignals(False)
            return

        elif cmd.startswith("http") or ".com" in cmd or ".org" in cmd or ".in" in cmd:
            webbrowser.open(cmd if cmd.startswith("http") else "https://" + cmd)
            self.hide()
            self.input.clear()
            return

        else:
            try:
                subprocess.Popen([cmd])
                self.hide()
                self.input.clear()
                # self.list_widget.hide()
            except:
                self.input.setText("not an executable try: firefox, code, etc")
            self.input.setFocus()

    def on_text_changed(self, text):
        self.list_widget.clear()
        self.page = 0
        if not text or text.startswith("="):
            # # self.list_widget.hide()
            return
        self.search_timer.start(200)  # Debounce: wait 200ms after last keypress

    def _do_search(self):
        text = self.input.text()
        # App search (cached)
        app_results = [
            (name, path, "app")
            for name, path in self.apps_cache
            if text.lower() in name.lower()
        ]
        # File/folder search (background)
        if text != self.fs_query:
            self.fs_query = text
            self.fs_results = []
            if self.fs_thread and self.fs_thread.is_alive():
                # Let the old thread finish, but don't use its results
                pass
            self.fs_worker = SearchWorker(text, os.path.expanduser("~"))
            self.fs_worker.results_ready.connect(self.on_fs_results_ready)
            self.fs_thread = threading.Thread(target=self.fs_worker.run)
            self.fs_thread.daemon = True
            self.fs_thread.start()
        else:
            self.show_results(app_results, self.fs_results)

    def on_fs_results_ready(self, results):
        self.fs_results = results
        app_results = [
            (name, path, "app")
            for name, path in self.apps_cache
            if self.fs_query.lower() in name.lower()
        ]
        self.show_results(app_results, self.fs_results)

    def show_results(self, app_results, fs_results):
        all_results = app_results + fs_results
        start = self.page * self.page_size
        end = start + self.page_size
        page_results = all_results[start:end]

        self.list_widget.clear()
        for name, path, tag in page_results:
            item = QListWidgetItem(f"{name} [{tag}]")
            item.setData(Qt.UserRole, (path, tag))
            self.list_widget.addItem(item)

        if end < len(all_results):
            show_more = QListWidgetItem("Show more...")
            show_more.setData(Qt.UserRole, ("show_more", "action"))
            self.list_widget.addItem(show_more)

        # Always show the list_widget, even if empty
        if not page_results and not (end < len(all_results)):
            item = QListWidgetItem("No files or apps found")
            item.setFlags(Qt.NoItemFlags)
            self.list_widget.addItem(item)
        self.list_widget.show()

    def item_selected(self, item):
        data = item.data(Qt.UserRole)
        if data == ("show_more", "action"):
            self.page += 1
            app_results = [
                (name, path, "app")
                for name, path in self.apps_cache
                if self.fs_query.lower() in name.lower()
            ]
            self.show_results(app_results, self.fs_results)
        else:
            path, tag = data
            if tag == "folder":
                subprocess.Popen(["xdg-open", path])
                self.hide()
                self.input.clear()
                # self.list_widget.hide()
            elif tag == "file":
                subprocess.Popen(["xdg-open", path])
                self.hide()
                self.input.clear()
                # self.list_widget.hide()
            elif tag == "app":
                self.input.setText(item.text().rsplit(" [", 1)[0])
                self.launch_command()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
            self.input.clear()
            # self.list_widget.hide()
        elif event.key() == Qt.Key_Down:
            if self.list_widget.isVisible():
                self.list_widget.setFocus()
                self.list_widget.setCurrentRow(0)
        else:
            super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if obj == self.list_widget and event.type() == event.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                current_item = self.list_widget.currentItem()
                if current_item:
                    self.item_selected(current_item)
                    return True
            elif event.key() == Qt.Key_Up:
                current_row = self.list_widget.currentRow()
                if current_row > 0:
                    self.list_widget.setCurrentRow(current_row - 1)
                return True
            elif event.key() == Qt.Key_Down:
                current_row = self.list_widget.currentRow()
                if current_row < self.list_widget.count() - 1:
                    self.list_widget.setCurrentRow(current_row + 1)
                return True
        return super().eventFilter(obj, event)

    def get_installed_apps(self):
        apps = []
        desktop_dirs = [
            "/usr/share/applications",
            os.path.expanduser("~/.local/share/applications"),
        ]
        for dir in desktop_dirs:
            for file in glob.glob(os.path.join(dir, "*.desktop")):
                try:
                    with open(file, "r") as f:
                        for line in f:
                            if line.startswith("Name="):
                                name = line.strip().split("=", 1)[1]
                                apps.append((name, file))
                                break
                except:
                    pass
        return apps

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_active and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_active = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = QuickLauncher()
    launcher.show()
    sys.exit(app.exec_())
