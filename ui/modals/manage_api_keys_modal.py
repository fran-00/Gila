import os

from dotenv import load_dotenv
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPixmap

from .parent_modal import Modal


class ManageAPIKeysModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Gestisci Chiavi API")
        self.api_keys = {
            "OpenAi": False,
            "Google": False,
            "Cohere": False
        }

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.set_icons()
        self.on_client_list_row("OpenAI")
        self.on_client_list_row("Google")
        self.on_client_list_row("Cohere")

    def on_stored_api_keys(self):
        load_dotenv()
        if os.getenv(f"OPENAI_API_KEY"):
            self.openai_key = True
        if os.getenv(f"GOOGLE_API_KEY"):
            self.openai_key = True
        if os.getenv(f"COHERE_API_KEY"):
            self.openai_key = True

    def on_client_list_row(self, client_name):
        row_layout = QHBoxLayout()
        label = QLabel(client_name)
        row_layout.addWidget(label)

        icon_label = QLabel()
        icon_label.setPixmap(self.red_icon)
        row_layout.addWidget(icon_label)

        modify_button = QPushButton("Modifica")
        row_layout.addWidget(modify_button)
        self.modal_layout.addLayout(row_layout)

    def set_icons(self):
        red_icon_path = "ui/icons/red-circle.svg"
        green_icon_path = "ui/icons/green-circle.svg"
        self.red_icon = QPixmap(red_icon_path)
        self.green_icon = QPixmap(green_icon_path)
