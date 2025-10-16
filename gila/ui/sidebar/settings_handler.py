import re

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSlider,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..utils import FileHandler as FH


class SettingsHandler(QObject):
    new_settings_to_controller = Signal(str, float, int, str, str, str, int, str)

    def __init__(self, parent_sidebar, current_settings):
        super().__init__()
        self.parent_cls = parent_cls
        self.current_settings = current_settings
        self.widget_container = QWidget(objectName="change_settings_widget")
        self._build_scroll_area()
        self._build_layout()

    def _build_scroll_area(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.widget_container)
        self.scroll_area.setWidgetResizable(True)

    def _build_layout(self):
        self.layout = QVBoxLayout(self.widget_container)
        self.layout.setAlignment(Qt.Alignment.AlignTop)
        self._build_llms_settings()
        self.add_line_separator(self.layout)
        self._build_temp_settings()
        self._build_reasoning_settings()
        self._build_img_size_settings()
        self.add_line_separator(self.layout)
        self._build_max_tokens_settings()
        self._build_img_quality_settings()
        self._build_img_num_settings()
        self.add_line_separator(self.layout)
        self._build_sys_msg_settings()
        self.llms_combobox.currentTextChanged.connect(self._change_needed_settings)
        self._on_settings_changed()
        self.load_settings_from_json()

        self._check_if_img()
        self._check_if_reasoner()

    def add_line_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setMaximumHeight(1)
        self.parent_sidebar.window.assign_css_class(line, "line_separator")
        layout.addWidget(line)

    def _show_img_settings(self):
        self.img_size_w.show()
        self.img_quality_w.show()
        self.img_num_w.show()
        self.temp_w.hide()
        self.reasoning_w.hide()
        self.max_tokens_w.hide()
        self.sys_msg_w.hide()

    def _hide_img_settings(self):
        self.img_size_w.hide()
        self.img_quality_w.hide()
        self.img_num_w.hide()
        self.temp_w.show()
        self.max_tokens_w.show()
        self.sys_msg_w.show()

    def _show_advanced_settings(self):
        self.temp_w.hide()
        self.reasoning_w.show()
        # o1-mini model currently doesn't support reasoning_effort and system message
        if self.selected_llm == "o1-mini":
            self.reasoning_w.hide()
            self.sys_msg_w.hide()

    def _hide_advanced_settings(self):
        self.temp_w.show()
        self.reasoning_w.hide()

    def send_new_settings_to_controller(self):
        """ Sends new settings to controller: signal is triggered when
            Confirm Button is pressed
        """
        selected_llm = self.llms_combobox.currentText()
        selected_temperature = self.temp_slider.value()
        selected_reasoning_effort = self.reasoning_group.checkedButton().text() if self.reasoning_group.checkedButton() else None
        selected_max_tokens = self.tokens_slider.value()
        selected_sys_msg = self.sys_msg_input.toPlainText()
        selected_img_size = self.size_group.checkedButton().text() if self.size_group.checkedButton() else None
        selected_img_quality = self.quality_group.checkedButton().text() if self.quality_group.checkedButton() else None
        selected_img_num = self.img_num_slider.value()
        self.new_settings_to_controller.emit(
            selected_llm,
            selected_temperature,
            selected_max_tokens,
            selected_sys_msg,
            selected_img_size,
            selected_img_quality,
            selected_img_num,
            selected_reasoning_effort,
        )

    def _change_needed_settings(self):
        """ Adjusts token limits and temperature range, based on a given model. """
        self.selected_llm = self.llms_combobox.currentText()
        limits = self._get_limits_from_json()
        default_tokens = [4096, 1]
        max_tokens, max_temp = limits.get(self.selected_llm, default_tokens)
        self._check_if_img()
        self._check_if_reasoner()
        self.tokens_slider.setMaximum(max_tokens)
        self.max_tokens_lbl.setText(str(max_tokens))
        self.temp_slider.setMaximum(20 if max_temp == 2 else 10)
        self.max_temp_lbl.setText(str(max_temp))

    def _get_limits_from_json(self):
        models_data = FH.load_file("storage/assets/json/models.json")
        return {model_name: data["limits"] for model_name, data in models_data.items()} if models_data else {}

    def _check_if_img(self):
        if re.match(r"^DALL-E \d+", self.selected_llm):
            self._show_img_settings()
        else:
            self._hide_img_settings()

        selected_size_button = self.size_group.checkedButton()
        if self.selected_llm in ["DALL-E 2"]:
            self.img_num_w.show()
            self.checkbox_256x256.show()
            self.checkbox_512x512.show()
            self.checkbox_1024x1792.hide()
            self.checkbox_1792x1024.hide()
            self.img_quality_w.hide()
            if selected_size_button in [self.checkbox_1024x1792, self.checkbox_1792x1024]:
                self.checkbox_1024x1024.setChecked(True)

        elif self.selected_llm in ["DALL-E 3"]:
            self.img_num_w.hide()
            self.checkbox_256x256.hide()
            self.checkbox_512x512.hide()
            self.checkbox_1024x1792.show()
            self.checkbox_1792x1024.show()
            self.checkbox_hd.show()
            if selected_size_button in [self.checkbox_256x256, self.checkbox_512x512]:
                self.checkbox_1024x1024.setChecked(True)

    def _check_if_reasoner(self):
        if re.match(r"^o\d+(-\w+)?$", self.selected_llm):
            self._show_advanced_settings()
            self.select_tokens_lbl.setText("Max Completion Tokens")
        elif re.match(r"^DALL-E \d+", self.selected_llm):
            pass
        else:
            self._hide_advanced_settings()
            self.select_tokens_lbl.setText("Max Tokens")

    def load_settings_from_json(self):
        """Load the saved settings from the JSON file and sets values"""
        settings = FH.load_file("storage/saved_settings.json")

        # Sets saved llm
        index = self.llms_combobox.findText(settings["llm_name"])
        if index != -1:
            self.llms_combobox.setCurrentIndex(index)
        # Sets temperature e max_tokens
        self.temp_slider.setValue(int(settings["temperature"] * 10))
        self.tokens_slider.setValue(int(settings["max_tokens"]))
        # Sets system_message
        self.sys_msg_input.setText(settings["system_message"])
        # Sets reasoning_effort
        reasoning_effort = settings.get("reasoning_effort", "")
        for button in self.reasoning_group.buttons():
            # Note: reasoning str is lowercase in the client
            if button.text() == reasoning_effort.capitalize():
                button.setChecked(True)
                break
        # Sets img_size
        img_size = settings.get("image_size", "")
        for button in self.size_group.buttons(): 
            if button.text() == img_size:
                button.setChecked(True)
                break
        # Sets img_quality
        img_quality = settings.get("image_quality", "")
        for button in self.quality_group.buttons(): 
            if button.text() == img_quality:
                button.setChecked(True)
                break
        # Update parameter limits based on the selected model
        self._change_needed_settings()

    def _on_settings_changed(self):
        """Connects settings widgets to send_new_settings_to_controller signal"""
        self.llms_combobox.currentIndexChanged.connect(self.send_new_settings_to_controller)
        self.temp_slider.valueChanged.connect(self.send_new_settings_to_controller)
        self.tokens_slider.valueChanged.connect(self.send_new_settings_to_controller)
        self.sys_msg_input.textChanged.connect(self.send_new_settings_to_controller)
        self.size_group.buttonClicked.connect(self.send_new_settings_to_controller)
        self.reasoning_group.buttonClicked.connect(self.send_new_settings_to_controller)
        self.quality_group.buttonClicked.connect(self.send_new_settings_to_controller)
        self.img_num_slider.valueChanged.connect(self.send_new_settings_to_controller)
