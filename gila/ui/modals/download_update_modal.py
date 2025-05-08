from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QProgressBar, QPushButton, QVBoxLayout

from .parent_modal import Modal


class DownloadUpdateModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Download Update")
        self._build_modal_layout()
        self.in_progress = True

    def _build_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self._build_modal_text_label()
        self.modal_text.setText("Downloading Update...")

        flags = self.windowFlags()
        self.setWindowFlags(flags & ~Qt.WindowCloseButtonHint)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.modal_layout.addWidget(self.progress_bar)

        # self.install_button = QPushButton("Install", self)
        # self.install_button.hide()
        # self.install_button.clicked.connect(lambda: self.request_update_installation())
        # self.modal_layout.addWidget(self.install_button)

        self.dismiss_button = QPushButton("Close", self)
        self.dismiss_button.hide()
        self.dismiss_button.clicked.connect(lambda: self.accept())
        self.modal_layout.addWidget(self.dismiss_button)

        self.window.set_cursor_pointer_for_buttons(self)

    @Slot(int)
    def show_download_progress_slot(self, percent):
        """ Slot
        Connected to one signal:
            - controller.download_progress_to_view
        """
        self.progress_bar.setValue(percent)

    @Slot()
    def show_download_finished_slot(self):
        """ Slot
        Connected to one signal:
            - controller.download_finished_to_view
        """
        self._download_finished(
            "The latest version has been downloaded. Please close this window and manually replace the executable. Automatic installation is currently under development."
        )

    @Slot(str)
    def show_updater_error_slot(self, error_msg):
        """ Slot
        Connected to one signal:
            - controller.updater_error_to_view
        """
        self._download_finished(f"Error:\n{error_msg}", error=True)

    def _download_finished(self, message: str, error: bool = False):
        self.in_progress = False
        self.modal_text.setText(message)

        if not error:
            self.progress_bar.hide()
            # self.install_button.show()
            self.dismiss_button.show()
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

    def request_update_installation(self):
        self.install_update_requested_to_controller.emit()
