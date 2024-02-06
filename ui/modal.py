from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton


class MissingAPIKeyModal(QDialog):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setWindowTitle("Chiave Mancante")
        layout = QVBoxLayout(self)
        self.line_edit = QLineEdit(self)
        layout.addWidget(self.line_edit)
        button = QPushButton("OK", self)
        button.clicked.connect(self.accept)
        layout.addWidget(button)
