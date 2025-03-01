from PySide6.QtCore import Signal, QUrl
from PySide6.QtGui import QAction, Qt
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import QFileDialog, QMenu, QTextEdit


class CustomTextEdit(QTextEdit):
    returnPressed = Signal()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.returnPressed.emit()
        else:
            super().keyPressEvent(event)


class CustomWebView(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_custom_menu)
        self.manager = QNetworkAccessManager(self)
        self._last_context_menu_pos = None

    def show_custom_menu(self, pos):
        self._last_context_menu_pos = pos
        # Detects if the element under the cursor is an image
        js = f"""
        (() => {{
            const elem = document.elementFromPoint({pos.x()}, {pos.y()});
            return elem?.tagName?.toLowerCase() === 'img' ? elem.src : null;
        }})();
        """
        self.page().runJavaScript(js, self.handle_context_menu_data)

    def handle_context_menu_data(self, result):
        menu = QMenu(self)

        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_selected_text)

        menu.addAction(copy_action)

        # If there is a result, it means that clicked element is an image
        if result:
            save_image_action = QAction("Save image", self)
            save_image_action.triggered.connect(lambda: self.save_image(result))
            menu.addAction(save_image_action)

        menu.exec(self.mapToGlobal(self._last_context_menu_pos))

    def copy_selected_text(self):
        self.page().triggerAction(QWebEnginePage.Copy)

    def save_image(self, image_url):
        url = QUrl(image_url)
        if not url.isValid():
            return
        default_filename = url.fileName() or "downloaded_image"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salva immagine",
            default_filename,
            "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)",
            options=QFileDialog.Options(),
        )
        if file_path:
            reply = self.manager.get(QNetworkRequest(url))
            reply.finished.connect(lambda: self.on_download_finished(reply, file_path))

    def on_download_finished(self, reply, file_path):
        # Read downloaded data and save them
        data = reply.readAll()
        with open(file_path, "wb") as f:
            f.write(bytes(data))
        reply.deleteLater()
