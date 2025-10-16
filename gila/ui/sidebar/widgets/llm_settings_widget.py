from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QSlider,
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
        self._build_temp_settings()

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

    def _build_temp_settings(self):
        """ Widget to adjust temperature settings """
        # Create inner widget and layout to contain temperature settings
        self.temp_w = QWidget()
        box_v = QVBoxLayout(self.temp_w)
        box_v.setContentsMargins(0, 0, 0, 0)

        # Create temperature lbl
        temp_lbl = QLabel("Temperature")
        self.parent_cls.parent_cls.window.assign_css_class(temp_lbl, "setting_name")
        temp_lbl.setAlignment(Qt.Alignment.AlignCenter)

        # Create widgets and slider's sub-layout
        temp_slider_sub_h = QHBoxLayout()
        min_temp_lbl = QLabel("0")
        self.max_temp_lbl = QLabel("1")
        self.temp_slider = QSlider(Qt.Horizontal)
        self.current_temp_lbl = QLabel("0")
        self.parent_cls.parent_cls.window.assign_css_class(self.current_temp_lbl, "current_value_lbl")

        # Adjust lbls settings and width
        self.current_temp_lbl.setAlignment(Qt.Alignment.AlignCenter)
        min_temp_lbl.setAlignment(Qt.Alignment.AlignRight | Qt.Alignment.AlignVCenter)
        min_temp_lbl.setFixedWidth(30)
        self.max_temp_lbl.setFixedWidth(30)
        temp_slider_sub_h.setStretchFactor(min_temp_lbl, 0)
        temp_slider_sub_h.setStretchFactor(self.temp_slider, 1)
        temp_slider_sub_h.setStretchFactor(self.max_temp_lbl, 0)
        self.parent_cls.parent_cls.window.assign_css_class(min_temp_lbl, "slider_value_lbl")
        self.parent_cls.parent_cls.window.assign_css_class(self.max_temp_lbl, "slider_value_lbl")

        # Adjust slider's settings
        self.temp_slider.setMinimum(0)
        self.temp_slider.setMaximum(10)
        self.temp_slider.setTickInterval(1)
        self.temp_slider.setSingleStep(1)
        self.temp_slider.valueChanged.connect(self._on_temperature_settings_changed)

        # Add widgets and slider to temperature slider sub layout
        temp_slider_sub_h.addWidget(min_temp_lbl)
        temp_slider_sub_h.addWidget(self.temp_slider)
        temp_slider_sub_h.addWidget(self.max_temp_lbl)

        # Add lbl, slider sub layout and current value to temperature inner layout
        box_v.addWidget(temp_lbl)
        box_v.addLayout(temp_slider_sub_h)
        box_v.addWidget(self.current_temp_lbl)

        # Add temperture inner widget to main layout
        self.layout.addWidget(self.temp_w)

    def _on_temperature_settings_changed(self):
        selected_temp_value = self.temp_slider.value() / 10
        self.current_temp_lbl.setText(str(selected_temp_value))
