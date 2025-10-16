import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QSlider,
    QTextEdit,
    QWidget,
    QVBoxLayout,
)


class LLMSettingsWidget(QWidget):

    def __init__(self, parent_handler):
        super().__init__()
        self.parent_handler = parent_handler
        self._build_layout()

    def _build_layout(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.Alignment.AlignTop)
        self._build_temp_settings()
        self._build_reasoning_settings()
        self.parent_handler.add_line_separator(self.layout)
        self._build_max_tokens_settings()
        self.parent_handler.add_line_separator(self.layout)
        self._build_sys_msg_settings()

    def _build_temp_settings(self):
        """ Widget to adjust temperature settings """
        # Create inner widget and layout to contain temperature settings
        self.temp_w = QWidget()
        box_v = QVBoxLayout(self.temp_w)
        box_v.setContentsMargins(0, 0, 0, 0)

        # Create temperature lbl
        temp_lbl = QLabel("Temperature")
        self.parent_handler.parent_sidebar.window.assign_css_class(temp_lbl, "setting_name")
        temp_lbl.setAlignment(Qt.Alignment.AlignCenter)

        # Create widgets and slider's sub-layout
        temp_slider_sub_h = QHBoxLayout()
        min_temp_lbl = QLabel("0")
        self.max_temp_lbl = QLabel("1")
        self.temp_slider = QSlider(Qt.Horizontal)
        self.current_temp_lbl = QLabel("0")
        self.parent_handler.parent_sidebar.window.assign_css_class(self.current_temp_lbl, "current_value_lbl")

        # Adjust lbls settings and width
        self.current_temp_lbl.setAlignment(Qt.Alignment.AlignCenter)
        min_temp_lbl.setAlignment(Qt.Alignment.AlignRight | Qt.Alignment.AlignVCenter)
        min_temp_lbl.setFixedWidth(30)
        self.max_temp_lbl.setFixedWidth(30)
        temp_slider_sub_h.setStretchFactor(min_temp_lbl, 0)
        temp_slider_sub_h.setStretchFactor(self.temp_slider, 1)
        temp_slider_sub_h.setStretchFactor(self.max_temp_lbl, 0)
        self.parent_handler.parent_sidebar.window.assign_css_class(min_temp_lbl, "slider_value_lbl")
        self.parent_handler.parent_sidebar.window.assign_css_class(self.max_temp_lbl, "slider_value_lbl")

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

    def _build_max_tokens_settings(self):
        """ Widget to adjust max tokens settings """
        # Create inner widget and layout to contain max tokens settings
        self.max_tokens_w = QWidget()
        box_v = QVBoxLayout(self.max_tokens_w)
        box_v.setContentsMargins(0, 0, 0, 0)
        # Create max_tokens label
        self.select_tokens_lbl = QLabel("Max Tokens")
        self.parent_handler.parent_sidebar.window.assign_css_class(self.select_tokens_lbl, "setting_name")
        self.select_tokens_lbl.setAlignment(Qt.Alignment.AlignCenter)
        # Create widgets and slider's sub-layout
        tokens_slider_sub_h = QHBoxLayout()
        min_tokens_lbl = QLabel("150")
        self.max_tokens_lbl = QLabel("4096")
        self.tokens_slider = QSlider(Qt.Horizontal)
        self.max_tokens_current_value_lbl = QLabel("1000")
        self.parent_handler.parent_sidebar.window.assign_css_class(self.max_tokens_current_value_lbl, "current_value_lbl")
        # Adjust labels settings and width
        self.max_tokens_current_value_lbl.setAlignment(Qt.Alignment.AlignCenter)
        min_tokens_lbl.setAlignment(Qt.Alignment.AlignRight | Qt.Alignment.AlignVCenter)
        min_tokens_lbl.setFixedWidth(30)
        self.max_tokens_lbl.setFixedWidth(30)
        tokens_slider_sub_h.setStretchFactor(min_tokens_lbl, 0)
        tokens_slider_sub_h.setStretchFactor(self.tokens_slider, 1)
        tokens_slider_sub_h.setStretchFactor(self.max_tokens_lbl, 0)
        self.parent_handler.parent_sidebar.window.assign_css_class(min_tokens_lbl, "slider_value_lbl")
        self.parent_handler.parent_sidebar.window.assign_css_class(self.max_tokens_lbl, "slider_value_lbl")
        # Adjust slider's settings
        self.tokens_slider.setMinimum(150)
        self.tokens_slider.setMaximum(4096)
        self.tokens_slider.setTickInterval(100)
        self.tokens_slider.setSingleStep(100)
        self.tokens_slider.valueChanged.connect(self._on_max_tokens_settings_changed)
        # Add widgets and slider to max_tokens slider sub layout
        tokens_slider_sub_h.addWidget(min_tokens_lbl)
        tokens_slider_sub_h.addWidget(self.tokens_slider)
        tokens_slider_sub_h.addWidget(self.max_tokens_lbl)
        # Add lbl, slider sub layout and current value to max tokens inner layout
        box_v.addWidget(self.select_tokens_lbl)
        box_v.addLayout(tokens_slider_sub_h)
        box_v.addWidget(self.max_tokens_current_value_lbl)
        # Add temperture inner widget to main layout
        self.layout.addWidget(self.max_tokens_w)

    def _on_max_tokens_settings_changed(self):
        selected_max_tokens_value = self.tokens_slider.value()
        self.max_tokens_current_value_lbl.setText(str(selected_max_tokens_value))

    def _build_sys_msg_settings(self):
        """ Widget to adjust system message setting """
        # Create inner widget and layout to contain system message
        self.sys_msg_w = QWidget()
        box_v = QVBoxLayout(self.sys_msg_w)
        box_v.setContentsMargins(0, 0, 0, 0)
        # Create system message lbl
        sys_msg_lbl = QLabel("System Message")
        self.parent_handler.parent_sidebar.window.assign_css_class(sys_msg_lbl, "setting_name")
        sys_msg_lbl.setAlignment(Qt.Alignment.AlignCenter)
        # Create system message QTextEdit
        self.sys_msg_input = QTextEdit(objectName="sys_msg_widget")
        # Add lbl and QTextEdit widget to system message inner layout
        box_v.addWidget(sys_msg_lbl)
        box_v.addWidget(self.sys_msg_input)
        # Add system message inner widget to main layout
        self.layout.addWidget(self.sys_msg_w)

    def _build_reasoning_settings(self):
        """ Widget to adjust reasoning effort settings """
        # Create inner widget and layout to contain reasoning effort settings
        self.reasoning_w = QWidget()
        box_v = QVBoxLayout(self.reasoning_w)
        box_v.setContentsMargins(0, 0, 0, 0)
        # Create reasoning effort lbl
        select_reasoning_lbl = QLabel("Reasoning Effort")
        self.parent_handler.parent_sidebar.window.assign_css_class(select_reasoning_lbl, "setting_name")
        select_reasoning_lbl.setAlignment(Qt.Alignment.AlignCenter)
        # Create widget's button group with checkboxes
        self.reasoning_group = QButtonGroup(self)
        self.reasoning_group.setExclusive(True)
        self.checkbox_low = QCheckBox("Low")
        self.checkbox_medium = QCheckBox("Medium")
        self.checkbox_high = QCheckBox("High")
        self.reasoning_group.addButton(self.checkbox_low)
        self.reasoning_group.addButton(self.checkbox_medium)
        self.reasoning_group.addButton(self.checkbox_high)
        # Add lbl and checkboxes to reasoning effort inner layout
        box_v.addWidget(select_reasoning_lbl)
        box_v.addWidget(self.checkbox_low)
        box_v.addWidget(self.checkbox_medium)
        box_v.addWidget(self.checkbox_high)
        # Add reasoning effort inner widget to main layout
        self.layout.addWidget(self.reasoning_w)

    def check_if_reasoner(self):
        if re.match(r"^o\d+(-\w+)?$", self.parent_handler.selected_llm):
            self._show_advanced_settings()
            self.select_tokens_lbl.setText("Max Completion Tokens")
        elif re.match(r"^DALL-E \d+", self.parent_handler.selected_llm):
            pass
        else:
            self._hide_advanced_settings()
            self.select_tokens_lbl.setText("Max Tokens")

    def _show_advanced_settings(self):
        self.temp_w.hide()
        self.reasoning_w.show()
        # o1-mini model currently doesn't support reasoning_effort and system message
        if self.parent_handler.selected_llm == "o1-mini":
            self.reasoning_w.hide()
            self.sys_msg_w.hide()

    def _hide_advanced_settings(self):
        self.temp_w.show()
        self.reasoning_w.hide()
