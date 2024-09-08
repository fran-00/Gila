from PySide6.QtWidgets import QVBoxLayout

from .parent_modal import Modal


class WarningModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Avviso")
        self.on_modal_layout()

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.on_modal_text()
        self.on_dismiss_button()

    def on_label(self, message):
        self.modal_text.setText(message)

    def on_no_internet_connection_label(self):
        self.modal_text.setText("Your computer is not connected to the internet, please check your connection and try again.")

    def on_key_is_valid_label(self):
        self.modal_text.setText("The API key is valid and has been successfully registered!")

    def on_key_is_not_valid_label(self):
        self.modal_text.setText("The API key you entered is not valid, please try again.")

    def on_deleting_current_chat_label(self):
        self.modal_text.setText("You can't delete an ongoing chat!\nStart a new conversation or load another one and try again.")
