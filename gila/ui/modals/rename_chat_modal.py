from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLineEdit

from .parent_modal import Modal


class RenameChatModal(Modal):

    def __init__(self, window, parent_class):
        super().__init__(window)
        self.setWindowTitle("Rename Chat")
        self._build_modal_layout()
        self.parent_class = parent_class

    def _build_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self._build_modal_text_label()
        self.modal_text.setText("Enter a new name for the saved chat.")
        self._build_new_name_entry()
        self._build_confirm_button()
        self.window.set_cursor_pointer_for_buttons(self)

    def _build_confirm_button(self):
        self.modal_button = QPushButton("Ok", self)
        self.modal_button.clicked.connect(lambda: self.parent_class.rename_stored_chat(self.new_name_entry.text()))
        self.modal_button.clicked.connect(self.accept)
        self.modal_layout.addWidget(self.modal_button)

    def _build_new_name_entry(self):
        self.new_name_entry = QLineEdit()
        self.new_name_entry.setMaxLength(20)
        self.modal_layout.addWidget(self.new_name_entry)
