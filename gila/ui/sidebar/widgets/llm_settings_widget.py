from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
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
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.Alignment.AlignTop)
        self._build_llms_settings()
        self.parent_cls.add_line_separator(self.layout)

    def _build_llms_settings(self):
        """ Creates ComboBox with llms list """
        select_llm_lbl = QLabel("Model")
        self.parent_cls.parent_cls.window.assign_css_class(select_llm_lbl, "setting_name")
        select_llm_lbl.setAlignment(Qt.Alignment.AlignCenter)
        self.llms_combobox = QComboBox()
        for llm in self.parent_cls.current_settings.llms:
            self.llms_combobox.addItem(llm)
        self.llms_combobox.setCurrentIndex(-1)
        self.layout.addWidget(select_llm_lbl)
        self.layout.addWidget(self.llms_combobox)
