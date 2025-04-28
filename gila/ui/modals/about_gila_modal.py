from PySide6.QtGui import Qt
from PySide6.QtWidgets import QVBoxLayout, QTextEdit

from .parent_modal import Modal
from ..utils import FileHandler as FH


class AboutGilaModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("About Gila")
        self._build_modal_layout()
        self.resize(800, 600)

    def _build_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self._build_about_text()
        self._build_dismiss_button()
        self.window.set_cursor_pointer_for_buttons(self)

    def _build_about_text(self):
        """ Parse an HTML file to show info to user """
        html_content = FH.load_file("storage/assets/html/about.html", encoding="utf-8")
        self.text_edit = QTextEdit()
        self.text_edit.setHtml(html_content)
        self.text_edit.setReadOnly(True)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.modal_layout.addWidget(self.text_edit)
