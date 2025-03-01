from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, Qt
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMenu, QTextEdit


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

    def show_custom_menu(self, pos):
        menu = QMenu(self)

        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_selected_text)

        menu.addAction(copy_action)
        menu.exec(self.mapToGlobal(pos))

    def copy_selected_text(self):
        self.page().triggerAction(QWebEnginePage.Copy)
