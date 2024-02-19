from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton

from .parent_modal import Modal


class WarningModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Avviso")
        self.on_modal_layout()

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.modal_text = QLabel("Messaggio di avviso da sovrascrivere.")
        self.modal_layout.addWidget(self.modal_text)
        self.on_dismiss_button()

    def on_dismiss_button(self):
        self.modal_button = QPushButton("OK", self)
        self.modal_button.clicked.connect(self.accept)
        self.modal_layout.addWidget(self.modal_button)

    def on_no_internet_connection_label(self):
        self.modal_text.setText("Il computer non è connesso ad internet, controlla la connessione e riprova.")
