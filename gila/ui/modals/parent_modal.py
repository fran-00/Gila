from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QPushButton, QLabel


class Modal(QDialog):
    api_key_to_controller = Signal(str, str)

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.resize(300, 100)
        self.setStyleSheet(self.load_css_file())

    def load_css_file(self):
        """ Loads CSS File to apply style to Modal Window """
        with open("storage/assets/modal-styles.css", "r") as file:
            return file.read()

    def on_modal_text(self):
        self.modal_text = QLabel("Messaggio da sovrascrivere.", objectName="modal_text")
        self.modal_text.setWordWrap(True)
        self.modal_layout.addWidget(self.modal_text)

    def on_dismiss_button(self):
        self.modal_button = QPushButton("OK", self)
        self.modal_button.clicked.connect(self.accept)
        self.modal_layout.addWidget(self.modal_button)
