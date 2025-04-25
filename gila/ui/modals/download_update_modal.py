from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QProgressBar, QPushButton, QVBoxLayout

from .parent_modal import Modal


class DownloadUpdateModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Download Update")
        self.on_modal_layout()
        self.in_progress = True

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.on_modal_text()
        self.modal_text.setText("Downloading Update...")

        flags = self.windowFlags()
        self.setWindowFlags(flags & ~Qt.WindowCloseButtonHint)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.modal_layout.addWidget(self.progress_bar)

        self.dismiss_button = QPushButton("Cancel", self)
        # self.dismiss_button.clicked.connect(self.reject)
        self.dismiss_button.clicked.connect(lambda: self.request_to_cancel_download())
        self.modal_layout.addWidget(self.dismiss_button)

        self.window.set_cursor_pointer_for_buttons(self)

    @Slot(int)
    def on_show_download_progress_slot(self, percent):
        """ Slot
        Connected to one signal:
            - controller.download_progress_to_view
        """
        self.progress_bar.setValue(percent)

    @Slot(str)
    def on_show_download_finished_slot(self, downloaded_path):
        """ Slot
        Connected to one signal:
            - controller.download_finished_to_view
        """
        pass

    @Slot(str)
    def on_show_download_error_slot(self, error_msg):
        """ Slot
        Connected to one signal:
            - controller.download_error_to_view
        """
        pass

    def on_download_finished(self, message: str, error: bool = False):
        self.in_progress = False
        self.modal_text.setText(message)

        if not error:
            self.progress_bar.hide()
        else:
            self.progress_bar.setEnabled(False)

        self.dismiss_button.show()
        flags = self.windowFlags()
        self.setWindowFlags(flags | Qt.WindowCloseButtonHint)
        self.show()

    def closeEvent(self, event):
        """If the dialog receives a close attempt (Alt+F4) while the download is
        in progress, ignore it; otherwise let it run.
        """
        if self.in_progress:
            event.ignore()
        else:
            super().closeEvent(event)
