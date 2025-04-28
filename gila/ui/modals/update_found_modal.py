from PySide6.QtWidgets import QVBoxLayout, QPushButton

from .parent_modal import Modal


class UpdateFoundModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Update found!")
        self._build_modal_layout()

    def _build_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.on_modal_text()
        self.modal_text.setText("A new update is available, do you want to download it?")
        self.on_confirm_button()
        self.on_dismiss_button()
        self.dismiss_button.setText("Close")
        self.window.set_cursor_pointer_for_buttons(self)

    def on_confirm_button(self):
        self.modal_button = QPushButton("Download", self)
        self.modal_button.clicked.connect(self.accept)
        self.modal_button.clicked.connect(lambda: self.download_update())
        self.modal_layout.addWidget(self.modal_button)

    def download_update(self):
        self.download_update_requested.emit()
