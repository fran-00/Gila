from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QDialog, QProgressBar, QLabel


class DownloadDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gila Updater")
        self.resize(400, 250)
        self.setStyleSheet(self.load_css_file())
        self.on_modal_layout()

    def load_css_file(self):
        """ Loads CSS File to apply style to Modal Window """
        with open("storage/assets/modal-styles.css", "r") as file:
            return file.read()

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.on_modal_text()
        self.on_progress_bar()

    def on_modal_text(self):
        self.modal_text = QLabel("Sto aggiornando...", objectName="modal_text")
        self.modal_text.setWordWrap(True)
        self.modal_layout.addWidget(self.modal_text)

    def on_progress_bar(self):
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.percent_label = QLabel("0%")
        self.percent_label.setAlignment(Qt.AlignCenter)
        self.modal_layout.addWidget(self.progress_bar)
        self.modal_layout.addWidget(self.percent_label)
