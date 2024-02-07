from PySide6.QtWidgets import QStatusBar
from PySide6.QtCore import QObject, Slot


class StatusBar(QObject):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.status_bar = QStatusBar()
        self.messages_history = []

    @Slot(str)
    def on_status_update_slot(self, status):
        """ Slot
        Connected to one signal:
            - controller.update_status_bar
        Shows a message on the status bar
        """
        self.messages_history.append(status)
        self.status_bar.showMessage(status)
