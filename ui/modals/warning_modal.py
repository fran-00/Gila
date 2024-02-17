from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton

from .parent_modal import Modal


class WarningModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Attenzione")
        self.on_modal_layout()
