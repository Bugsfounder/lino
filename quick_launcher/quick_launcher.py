import threading
from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QApplication,
    QListWidget,
    QListWidgetItem,
    QLabel,
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import subprocess
import webbrowser
from chatterbot import ChatBot
import sys
import os
import glob


class SearchWorker(QObject):
    results_ready = pyqtSignal(list)

    def __init__(self, query, root):
        super().__init__()
        self.query = query
        self.root = root
        self.user_uid = os.getuid()

    def run(self):
        results = []
        for dirpath, dirnames, filenames in os.walk(self.root):
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
        self.bot = ChatBot("LinoBot", read_only=True)
        self.setWindowTitle("Lino Quick Launcher")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(600, 300, 400, 180)
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        x = (rect.width() - self.width()) // 2
        y = (rect.height() - self.height()) // 2
        self.move(x, y)

        self.input = QLineEdit(self)
        self.input.setGeometry(10, 10, 380, 30)
        self.input.setPlaceholderText("Type to launch... (e.g., firefox)")
        self.input.returnPressed.connect(self.launch_command)
        self.input.textChanged.connect(self.update_dropdown)
        self.input.setFocus()

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(10, 45, 380, 100)
        self.list_widget.hide()
        self.list_widget.itemClicked.connect(self.item_selected)
        self.list_widget.installEventFilter(self)

        self.ai_response = QLabel(self)
        self.ai_response.setGeometry(10, 45, 380, 120)
        self.ai_response.setWordWrap(True)
        self.ai_response.setStyleSheet(
            "background-color: #fff; color: #000; padding: 5px; border: 1px solid #ccc;"
        )
        self.ai_response.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.ai_response.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.ai_response.hide()

        # Caching and paging
        self.apps_cache = self.get_installed_apps()
        self.fs_results = []
        self.fs_query = ""
        self.fs_thread = None
        self.fs_worker = None
        self.page = 0
        self.page_size = 5

    def launch_command(self):
        cmd = self.input.text().strip()
        self.ai_response.hide()

        if cmd.startswith("="):
            try:
                result = eval(cmd[1:].strip())
                self.input.blockSignals(
                    True
                )  # Block signals to prevent update_dropdown
                self.input.setText(str(result))
                self.input.blockSignals(False)  # Re-enable signals
            except:
                self.input.blockSignals(True)
                self.input.setText("Invalid Expression")
                self.input.blockSignals(False)
            return

        elif cmd.startswith("?"):
            query = cmd[1:].strip().lower()
            try:
                response = str(self.bot.get_response(query))
                self.ai_response.setText(response)
                self.ai_response.show()
                self.ai_response.raise_()
                self.ai_response.repaint()
            except:
                self.ai_response.setText("Sorry, I didn't get that.")
                self.ai_response.show()
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
                self.list_widget.hide()
            except:
                self.input.setText("Command Failed")
            self.input.setFocus()

    def update_dropdown(self, text):
        self.ai_response.hide()
        self.list_widget.clear()
        self.page = 0

        if not text or text.startswith("=") or text.startswith("?"):
            self.list_widget.hide()
            return
        else:
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
                self.fs_thread.daemon = True  # Add this line
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

        if page_results or (end < len(all_results)):
            self.list_widget.show()
        else:
            self.list_widget.hide()

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
                # Open folder in Nautilus or default file manager
                subprocess.Popen(["xdg-open", path])
                self.hide()
                self.input.clear()
                self.list_widget.hide()
            elif tag == "file":
                # Open file in default text editor
                subprocess.Popen(["xdg-open", path])
                self.hide()
                self.input.clear()
                self.list_widget.hide()
            elif tag == "app":
                # Launch app as before
                self.input.setText(item.text().rsplit(" [", 1)[0])
                self.launch_command()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
            self.input.clear()
            self.list_widget.hide()
            self.ai_response.hide()
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = QuickLauncher()
    launcher.show()
    sys.exit(app.exec_())
