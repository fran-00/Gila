from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Signal


class MissingAPIKeyModal(QDialog):
    api_key_to_controller = Signal(str)

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setWindowTitle("Chiave Mancante")
        self.setStyleSheet(self.load_css_file())
        self.on_modal_layout()

    def load_css_file(self):
        with open("ui/styles.css", "r") as file:
            return file.read()

    def on_modal_layout(self):
        self.modal_layout = QVBoxLayout(self)
        modal_text = QLabel(f"Inserisci l'API Key")
        self.modal_layout.addWidget(modal_text)
        self.modal_entry_line = QLineEdit(self)
        self.modal_layout.addWidget(self.modal_entry_line)
        modal_button = QPushButton("OK", self)
        modal_button.clicked.connect(self.process_api_key)
        modal_button.clicked.connect(self.accept)
        self.modal_layout.addWidget(modal_button)

    def process_api_key(self):
        api_key = self.modal_entry_line.text().strip()
        self.api_key_to_controller.emit(api_key)
        self.modal_entry_line.clear()
