from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)


class LLMSettingsWidget(QWidget):

    settings_changed = Signal()

    def __init__(self, parent_cls):
        super().__init__()
        self.parent_cls = parent_cls
        self._build_layout()

    def _build_layout(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.Alignment.AlignTop)
