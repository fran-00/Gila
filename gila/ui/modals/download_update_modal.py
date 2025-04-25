from PySide6.QtCore import Slot
from PySide6.QtWidgets import QVBoxLayout, QPushButton

from .parent_modal import Modal


class DownloadUpdateModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Download Update")
        self.on_modal_layout()

    @Slot(int)
    def on_show_download_progress_slot(self, percent):
        """ Slot
        Connected to one signal:
            - controller.download_progress_to_view
        """
        pass

    @Slot(str)
    def on_show_download_finished_slot(self, downloaded_path):
        """ Slot
        Connected to one signal:
            - controller.download_finished_to_view
        """
        pass

    @Slot(str)
    def on_show_download_error_slot(self, error_msg):
        """ Slot
        Connected to one signal:
            - controller.download_error_to_view
        """
        pass
