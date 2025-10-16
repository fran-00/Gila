from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)


class ImageSettingsWidget(QWidget):

    settings_changed_signal = Signal()

    def __init__(self, parent_handler):
        super().__init__()
        self.parent_handler = parent_handler
        self._build_layout()

    def _build_layout(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.Alignment.AlignTop)

    def _build_image_size_settings(self):
        pass
