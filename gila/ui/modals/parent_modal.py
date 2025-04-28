from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QPushButton, QLabel, QFrame

from ..utils import FileHandler as FH


class Modal(QDialog):
    api_key_to_controller = Signal(str, str)
    download_update_requested = Signal()
    cancel_download_requested_to_controller = Signal()
    install_update_requested_to_controller = Signal()

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.resize(430, 200)
        self.setStyleSheet(self._load_css_file())

    def _load_css_file(self):
        """ Loads CSS File to apply style to Modal Window """
        return FH.load_file("storage/assets/css/styles.css", encoding="utf-8")

    def _build_modal_text_label(self):
        self.modal_text = QLabel("Message to overwrite.", objectName="modal_text")
        self.modal_text.setMaximumWidth(400)
        self.modal_text.setWordWrap(True)
        self.modal_layout.addWidget(self.modal_text)

    def _build_dismiss_button(self):
        self.dismiss_button = QPushButton("OK", self)
        self.dismiss_button.clicked.connect(self.accept)
        self.modal_layout.addWidget(self.dismiss_button)

    def add_line_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setMaximumHeight(1)
        self.window.assign_css_class(line, "line_separator")
        layout.addWidget(line)
