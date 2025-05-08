from PySide6.QtWidgets import QVBoxLayout

from .parent_modal import Modal


class WarningModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Info")
        self._build_modal_layout()

    def _build_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self._build_modal_text_label()
        self._build_dismiss_button()
        self.window.set_cursor_pointer_for_buttons(self)

    def on_label(self, message):
        self.modal_text.setText(message)

    def on_no_internet_connection_label(self):
        self.modal_text.setText("You are offline, please check your connection and try again.")

    def on_key_is_valid_label(self):
        self.modal_text.setText("The API key is valid and has been successfully registered!")

    def on_key_is_not_valid_label(self):
        self.modal_text.setText("The API key you entered is not valid, please try again.")

    def on_deleting_current_chat_label(self):
        self.modal_text.setText("You can't delete an ongoing chat!\nStart a new conversation or load another one and try again.")

    def on_update_not_fount_label(self):
        self.modal_text.setText("You already have the most up-to-date version of Gila.")
