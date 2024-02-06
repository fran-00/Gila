from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton


class MissingAPIKeyModal(QDialog):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setWindowTitle("Chiave Mancante")
        self.setStyleSheet(self.load_css_file())
        layout = QVBoxLayout(self)
        self.line_edit = QLineEdit(self)
        layout.addWidget(self.line_edit)
        button = QPushButton("OK", self)
        button.clicked.connect(self.accept)
        layout.addWidget(button)

    def load_css_file(self):
        with open("ui/styles.css", "r") as file:
            return file.read()
