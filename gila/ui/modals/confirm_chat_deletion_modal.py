from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from .parent_modal import Modal


class ConfirmChatDeletionModal(Modal):

    def __init__(self, window, parent_class):
        super().__init__(window)
        self.setWindowTitle("Cancellazione Chat")
        self.on_modal_layout()
        self.parent_class = parent_class

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.modal_text = QLabel("Sei sicuro di voler eliminare questa chat? Non sarà più possibile recuperarla!")
        self.modal_text.setWordWrap(True)
        self.modal_layout.addWidget(self.modal_text)
        self.buttons_layout = QHBoxLayout()
        self.modal_layout.addLayout(self.buttons_layout)
        self.on_confirm_button()
        self.on_refuse_button()

    def on_confirm_button(self):
        self.modal_button = QPushButton("Sì, elimina!", self)
        self.modal_button.clicked.connect(lambda: self.parent_class.delete_stored_chat_by_name())
        self.modal_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.modal_button)

    def on_refuse_button(self):
        self.modal_button = QPushButton("No, annulla", self)
        self.modal_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.modal_button)
