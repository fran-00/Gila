from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Signal, Slot


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
        self.on_modal_entry_line()
        self.on_modal_button()
        self.on_modal_wait_label()
        self.on_key_is_valid_label()
        self.on_key_is_not_valid_label()

    def on_modal_entry_line(self):
        modal_text = QLabel(f"Inserisci l'API Key")
        self.modal_layout.addWidget(modal_text)
        self.modal_entry_line = QLineEdit(self)
        self.modal_layout.addWidget(self.modal_entry_line)

    def on_modal_button(self):
        self.modal_button = QPushButton("OK", self)
        self.modal_button.clicked.connect(self.process_api_key)
        # modal_button.clicked.connect(self.accept)
        self.modal_layout.addWidget(self.modal_button)

    def on_modal_wait_label(self):
        self.wait_label = QLabel('Attendere...')
        self.wait_label.hide()
        self.modal_layout.addWidget(self.wait_label)

    def on_key_is_valid_label(self):
        self.key_valid_label = QLabel('La chiave inserita è valida ed è stata registata.')
        self.key_valid_label.hide()
        self.modal_layout.addWidget(self.key_valid_label)

    def on_key_is_not_valid_label(self):
        self.key_not_valid_label = QLabel('La chiave inserita non è valida, prova di nuovo o chiudi.')
        self.key_not_valid_label.hide()
        self.modal_layout.addWidget(self.key_not_valid_label)

    def process_api_key(self):
        self.key_valid_label.hide()
        self.key_not_valid_label.hide()
        api_key = self.modal_entry_line.text().strip()
        if api_key != "":
            self.wait_label.show()
            self.api_key_to_controller.emit(api_key)
            self.modal_entry_line.clear()

    @Slot(bool)
    def on_api_key_validation_slot(self, is_key_valid):
        self.wait_label.hide()
        self.modal_button.setEnabled(True)
        if is_key_valid is True:
            self.accept()
        else:
            print("api key is not valid!")
            self.close()
