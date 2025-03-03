from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QPushButton, QLabel, QFrame


class Modal(QDialog):
    api_key_to_controller = Signal(str, str)

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.resize(400, 150)
        self.setStyleSheet(self.load_css_file())

    def load_css_file(self):
        """ Loads CSS File to apply style to Modal Window """
        with open("storage/assets/css/styles.css", "r") as file:
            return file.read()

    def on_modal_text(self):
        self.modal_text = QLabel("Message to overwrite.", objectName="modal_text")
        self.modal_text.setWordWrap(True)
        self.modal_layout.addWidget(self.modal_text)

    def on_dismiss_button(self):
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
