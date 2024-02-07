from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Slot

from .parent_modal import Modal


class ManageAPIKeysModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Gestisci Chiavi API")

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
