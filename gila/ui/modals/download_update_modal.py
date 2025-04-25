from PySide6.QtCore import Slot
from PySide6.QtWidgets import QVBoxLayout, QPushButton

from .parent_modal import Modal


class DownloadUpdateModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Download Update")
        self.on_modal_layout()
