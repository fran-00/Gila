import os

from dotenv import load_dotenv
from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from .parent_modal import Modal
from ..utils import FileHandler as FH


class ManageAPIKeysModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Manage API Keys")
        self.api_keys = {
            "OpenAi": False,
            "Google": False,
            "DeepSeek": False,
            "Cohere": False,
            "Mistral": False,
            "Anthropic": False,
            "Arli": False,
            "Groq": False,
        }
        self._build_modal_layout()

    def _build_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self._build_modal_text_label()
        self.modal_text.setText("Edit saved API Keys (green dot) or add missing ones (red dot).")
        self.add_line_separator(self.modal_layout)
        self._set_icons()
        for key in self.api_keys.keys():
            self._build_client_list_row(key)
        self.window.set_cursor_pointer_for_buttons(self)

    def get_stored_api_keys(self):
        load_dotenv()
        for key in self.api_keys.keys():
            self.api_keys[f"{key}"] = bool(os.getenv(f"{key.upper()}_API_KEY"))

    def _build_client_list_row(self, client_name):
        row_layout = QHBoxLayout()
        label = QLabel(client_name)
        row_layout.addWidget(label)

        red_icon_label = QLabel(objectName=f"red_{client_name}_label")
        red_icon_label.setPixmap(self.red_icon)
        red_icon_label.setAlignment(Qt.Alignment.AlignCenter)
        green_icon_label = QLabel(objectName=f"green_{client_name}_label")
        green_icon_label.setPixmap(self.green_icon)
        green_icon_label.setAlignment(Qt.Alignment.AlignCenter)
        row_layout.addWidget(red_icon_label)
        row_layout.addWidget(green_icon_label)

        modify_button = QPushButton("Update")
        modify_button.clicked.connect(lambda: self.window.add_api_key_modal_slot(client_name))
        row_layout.addWidget(modify_button)
        self.modal_layout.addLayout(row_layout)

    def _set_icons(self):
        red_icon_path = FH.build_asset_path("storage/assets/icons/red-circle.svg")
        green_icon_path = FH.build_asset_path("storage/assets/icons/green-circle.svg")
        self.red_icon = QPixmap(red_icon_path)
        self.green_icon = QPixmap(green_icon_path)

    def update_labels(self):
        for key in self.api_keys.keys():
            red_label = self.findChild(QLabel, f"red_{key}_label")
            green_label = self.findChild(QLabel, f"green_{key}_label")
            if self.api_keys[f'{key}'] is False:
                red_label.show()
                green_label.hide()
            else:
                red_label.hide()
                green_label.show()
