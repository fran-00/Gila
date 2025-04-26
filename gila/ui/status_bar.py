from PySide6.QtCore import Slot
from PySide6.QtWidgets import QLabel, QStatusBar

from .utils import FileHandler as FH


class StatusBar(QStatusBar):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.messages_history = []

        self.version_label = QLabel(f"v1.0.0", objectName="version_label")
        self.addPermanentWidget(self.version_label)
        self.set_version()

    def set_version(self):
        data = FH.load_file("storage/assets/json/local_version.json")
        version = data.get("local_version")
        self.version_label.setText(f"{version}")

    @Slot(str)
    def on_status_update_slot(self, status):
        """ Slot
        Connected to one signal:
            - controller.update_status_bar
        Shows a message on the status bar
        """
        self.messages_history.append(status)
        self.showMessage(status)
