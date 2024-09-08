from PySide6.QtCore import Slot
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton

from .parent_modal import Modal


class AddAPIKeyModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.client_name = None
        self.setWindowTitle("Aggiungi API Key")
        self.on_modal_layout()

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.on_modal_text()
        self.modal_text.setText(f"Enter {self.client_name} API Key, it will be sent for verification.")
        self.add_line_separator(self.modal_layout)
        self.on_modal_entry_line()
        self.on_modal_button()
        self.on_modal_wait_label()

    def on_modal_entry_line(self):
        """ Add instructions text and an entry line """
        self.modal_entry_line = QLineEdit(self)
        self.modal_layout.addWidget(self.modal_entry_line)

    def update_modal_labels(self):
        self.modal_text.setText(f"Enter {self.client_name} API Key, it will be sent for verification.")

    def on_modal_button(self):
        """ Add a button so send API Key """
        self.modal_button = QPushButton("Submit", self)
        self.modal_button.clicked.connect(self.process_api_key)
        # modal_button.clicked.connect(self.accept)
        self.modal_layout.addWidget(self.modal_button)

    def on_modal_wait_label(self):
        """ Add a label when user must wait for API response """
        self.wait_label = QLabel('Wait...')
        self.wait_label.hide()
        self.modal_layout.addWidget(self.wait_label)

    def process_api_key(self):
        """ Gets API key and sends it as a Signal """
        api_key = self.modal_entry_line.text().strip()
        if api_key != "":
            self.wait_label.show()
            self.api_key_to_controller.emit(api_key, self.client_name)
            self.modal_entry_line.clear()

    @Slot(bool)
    def on_api_key_validation_slot(self, is_key_valid):
        """ Slot
        Connected to one signal:
            - controller.api_key_is_valid_to_view
        Shows a label saying if api key is valid
        """
        self.wait_label.hide()
        self.modal_button.setEnabled(True)
        if is_key_valid is True:
            self.accept()
            self.window.manage_api_keys_modal.accept()
            self.window.warning_modal.on_key_is_valid_label()
            self.window.warning_modal.exec_()
        else:
            self.window.warning_modal.on_key_is_not_valid_label()
            self.window.warning_modal.exec_()
