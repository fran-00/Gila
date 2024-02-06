from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton


class MissingAPIKeyModal(QDialog):

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
        modal_button.clicked.connect(self.accept)
        self.modal_layout.addWidget(modal_button)
