from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from .parent_modal import Modal


class ConfirmChatDeletionModal(Modal):

    def __init__(self, window, parent_cls):
        super().__init__(window)
        self.setWindowTitle("Delete saved chat")
        self._build_modal_layout()
        self.parent_cls = parent_cls

    def _build_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self._build_modal_text_label()
        self.modal_text.setText("Are you sure you want to delete this chat?")
        self.buttons_layout = QHBoxLayout()
        self.modal_layout.addLayout(self.buttons_layout)
        self._build_confirm_button()
        self._build_refuse_button()
        self.window.set_cursor_pointer_for_buttons(self)

    def _build_confirm_button(self):
        self.modal_button = QPushButton("Yes, delete it!", self)
        self.modal_button.clicked.connect(lambda: self.parent_cls.delete_stored_chat_by_name())
        self.modal_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.modal_button)

    def _build_refuse_button(self):
        self.modal_button = QPushButton("No, cancel.", self)
        self.modal_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.modal_button)
