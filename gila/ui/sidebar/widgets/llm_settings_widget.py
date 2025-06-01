from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)


class LLMSettingsWidget(QWidget):

    settings_changed = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def _build_layout(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.Alignment.AlignTop)
