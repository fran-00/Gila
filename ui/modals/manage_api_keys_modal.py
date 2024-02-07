import os

from dotenv import load_dotenv
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Slot

from .parent_modal import Modal


class ManageAPIKeysModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Gestisci Chiavi API")
        self.openai_key = False
        self.google_key = False
        self.cohere_key = False

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)

    def on_stored_api_keys(self):
        load_dotenv()
        if os.getenv(f"OPENAI_API_KEY"):
            self.openai_key = True
        if os.getenv(f"GOOGLE_API_KEY"):
            self.openai_key = True
        if os.getenv(f"COHERE_API_KEY"):
            self.openai_key = True
