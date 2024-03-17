from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLineEdit

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
        self.on_modal_text()
        self.modal_text.setText("Inserisci un nuovo nome per la chat salvata.")
        self.on_new_name_entry()
        self.on_confirm_button()

    def on_confirm_button(self):
        self.modal_button = QPushButton("Ok", self)
        self.modal_button.clicked.connect(lambda: self.parent_class.rename_stored_chat(self.new_name_entry.text()))
        self.modal_button.clicked.connect(self.accept)
        self.modal_layout.addWidget(self.modal_button)

    def on_new_name_entry(self):
        self.new_name_entry = QLineEdit()
        self.modal_layout.addWidget(self.new_name_entry)
