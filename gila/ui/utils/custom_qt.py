from PySide6.QtCore import Signal, QUrl, QMimeData
from PySide6.QtGui import QAction, Qt
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import QFileDialog, QMenu, QTextEdit


class CustomTextEdit(QTextEdit):
    """Custom text edit widget that extends QTextEdit to handle specific events.

    This class is used to manage the text box for entering prompts in the chat
    application.
    """
    returnPressed = Signal()

    def keyPressEvent(self, event):
        """Handle key press events to emit the returnPressed signal.
        
        Ensure that prompts can be submitted when the return or enter key is
        pressed, which is a behavior that, by default, is typically only
        available in QLineEdit widgets.

        If the pressed key is the return or enter key, this method emits 
        the `returnPressed` signal. For all other keys, it calls the 
        superclass implementation to ensure normal behavior.

        Args:
            event (QKeyEvent): The key event containing information about 
                               the key press.
        """
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.returnPressed.emit()
        else:
            super().keyPressEvent(event)

    def insertFromMimeData(self, source: QMimeData):
        """Insert plain text from the provided MIME data source.

        Prevent any text styling from being applied to text that is pasted into
        the prompt box overriding the default behavior to check if the MIME data
        contains text. If it does, the text is inserted as plain text into the
        text edit.

        Args:
            source (QMimeData): The MIME data source containing the data to 
                                be inserted.
        """
        if source.hasText():
            self.insertPlainText(source.text())


class CustomWebView(QWebEngineView):
    """Custom web view that extends QWebEngineView to implement a context menu.

    This class sets up a custom context menu for the web view, allowing 
    users to interact with specific elements in the rendered web content. 
    """
    def __init__(self):
        super().__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_custom_menu)
        self.manager = QNetworkAccessManager(self)
        self._last_context_menu_pos = None

    def show_custom_menu(self, pos):
        """Display a custom context menu at the specified position.

        This method is triggered when a context menu is requested. It stores 
        the position of the menu and executes a JavaScript snippet to check 
        if the element under the cursor is an image. If it is, the image's 
        source URL is retrieved for further actions.

        Args:
            pos (QPoint): The position where the context menu is requested.
        """
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
        """Handle the context menu actions based on the element clicked.

        Creates a context menu with options based on the user's right-click
        action. It includes a "copy" action for copying selected text. If the
        clicked element is an image (indicated by a non-null result), it adds
        an option to save the image.

        Displays the context menu at the last known position of the right-click
        event, converting the local position to a global position for proper
        menu placement.
        
        Args:
            result (str or None): The source URL of the image if the clicked 
                                  element is an image; otherwise, None.
        """
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
        """Copy the selected text from the web page to the clipboard.

        This method triggers the copy action on the current page, allowing 
        the user to copy any selected text directly from the web content.
        """
        self.page().triggerAction(QWebEnginePage.Copy)

    def save_image(self, image_url):
        """Save an image from the provided URL to a specified file location.

        Validates the given image URL and prompts the user to select a file
        location and name for saving the image. If the URL is valid, it
        initiates a network request to download the image and connects the
        download completion signal to handle the saved file.

        If the user selects a file path and the download finishes successfully, 
        the image is saved to the specified location.

        Args:
            image_url (str): The URL of the image to be saved.
        """
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
        """Handle the completion of the image download and saves the file.

        Called when the download of an image is finished: reads the downloaded
        data from the network reply and saves it to the specified file path.
        After saving, it cleans up the reply object to free resources.

        Args:
            reply (QNetworkReply): The network reply object containing the 
                                   downloaded image data.
            file_path (str): The file path where the image should be saved.
        """
        data = reply.readAll()
        with open(file_path, "wb") as f:
            f.write(bytes(data))
        reply.deleteLater()
