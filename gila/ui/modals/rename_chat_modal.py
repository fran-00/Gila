from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QLineEdit

from .parent_modal import Modal


class RenameChatModal(Modal):

    def __init__(self, window, parent_class):
        super().__init__(window)
        self.setWindowTitle("Rinomina Chat")
        self.on_modal_layout()
        self.parent_class = parent_class

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.modal_text = QLabel("Inserisci un nuovo nome per la chat salvata")
        self.modal_layout.addWidget(self.modal_text)
        self.on_dismiss_button()

    def on_confirm_button(self):
        self.modal_button = QPushButton("Ok", self)
        self.modal_button.clicked.connect(lambda: self.parent_class.delete_stored_chat_by_name())
        self.modal_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.modal_button)
