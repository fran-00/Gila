from PySide6.QtWidgets import QVBoxLayout, QPushButton

from .parent_modal import Modal


class UpdateFoundModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Aggiornamento trovato!")
        self.on_modal_layout()

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.on_modal_text()
        self.modal_text.setText("È disponibile un nuovo aggiornamento, vuoi scaricarlo?")
        self.on_confirm_button()
        self.on_dismiss_button()
        self.dismiss_button.setText("Chiudi")

    def on_confirm_button(self):
        self.modal_button = QPushButton("Scarica", self)
        self.modal_button.clicked.connect(lambda: self.download_update())
        self.modal_button.clicked.connect(self.accept)
        self.modal_layout.addWidget(self.modal_button)

    def download_update(self):
        print("Scarica aggiornamento")
