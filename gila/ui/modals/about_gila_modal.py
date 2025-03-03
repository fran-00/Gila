from PySide6.QtGui import Qt
from PySide6.QtWidgets import QVBoxLayout, QTextEdit

from .parent_modal import Modal
from ..utils import FileHandler as FH


class AboutGilaModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("About Gila")
        self.on_modal_layout()
        self.resize(800, 600)

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.on_about_text()
        self.on_dismiss_button()

    def on_about_text(self):
        """ Parse an HTML file to show info to user """
        html_content = FH.load_file("storage/about.html", encoding="utf-8")
        self.text_edit = QTextEdit()
        self.text_edit.setHtml(html_content)
        self.text_edit.setReadOnly(True)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.modal_layout.addWidget(self.text_edit)
