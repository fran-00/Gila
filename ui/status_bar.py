from PySide6.QtWidgets import QStatusBar
from PySide6.QtCore import QObject, Slot


class StatusBar(QObject):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.status_bar = QStatusBar()
        self.messages_history = []

    @Slot(str)
    def on_status_update(self, status):
        self.messages_history.append(status)
        self.status_bar.showMessage(status)
