from PySide6.QtGui import Qt
from PySide6.QtWidgets import QVBoxLayout, QTextEdit

from .parent_modal import Modal


class AboutGilaModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Informazioni su Gila")
        self.on_modal_layout()
        self.resize(800, 600)

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.on_modal_text()
        self.modal_text.setText("Informazioni su Gila")
        self.on_about_text()
        self.on_dismiss_button()

    def on_about_text(self):
        """ Parse an HTML file to show info to user """
        with open("storage/about.html", 'r') as file:
            html_content = file.read()
        self.text_edit = QTextEdit()
        self.text_edit.setHtml(html_content)
        self.text_edit.setReadOnly(True)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.modal_layout.addWidget(self.text_edit)
