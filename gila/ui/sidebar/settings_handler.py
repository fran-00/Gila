import re

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .widgets import ImageSettingsWidget, LLMSettingsWidget
from ..utils import FileHandler as FH


class SettingsHandler(QObject):
    new_settings_to_controller = Signal(str, float, int, str, str, str, int, str)

    def __init__(self, parent_sidebar, current_settings):
        super().__init__()
        self.parent_sidebar = parent_sidebar
        self.current_settings = current_settings
        self.widget_container = QWidget(objectName="change_settings_widget")
        self.llm_setting_widget = LLMSettingsWidget(self)
        self.image_setting_widget = ImageSettingsWidget(self)
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
        self.layout.addWidget(self.llm_setting_widget)
        self.layout.addWidget(self.image_setting_widget)

        self.llms_combobox.currentTextChanged.connect(
            self._change_needed_settings
        )
        self._on_settings_changed()
        self.load_settings_from_json()

        self._check_if_img()
        self.llm_setting_widget.check_if_reasoner()

    def _build_llms_settings(self):
        """ Creates ComboBox with llms list """
        select_llm_lbl = QLabel("Model")
        self.parent_sidebar.window.assign_css_class(select_llm_lbl, "setting_name")
        select_llm_lbl.setAlignment(Qt.Alignment.AlignCenter)
        self.llms_combobox = QComboBox()
        for llm in self.current_settings.llms:
            self.llms_combobox.addItem(llm)
        self.llms_combobox.setCurrentIndex(-1)
        self.layout.addWidget(select_llm_lbl)
        self.layout.addWidget(self.llms_combobox)

    def add_line_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setMaximumHeight(1)
        self.parent_sidebar.window.assign_css_class(line, "line_separator")
        layout.addWidget(line)

    def _show_img_settings(self):
        self.image_setting_widget.show()
        self.llm_setting_widget.hide()

    def _hide_img_settings(self):
        self.image_setting_widget.hide()
        self.llm_setting_widget.show()

    def send_new_settings_to_controller(self):
        """ Sends new settings to controller: signal is triggered when
            Confirm Button is pressed
        """
        selected_llm = self.llms_combobox.currentText()
        selected_temperature = self.llm_setting_widget.temp_slider.value()
        selected_reasoning_effort = self.llm_setting_widget.reasoning_group.checkedButton().text() if self.llm_setting_widget.reasoning_group.checkedButton() else None
        selected_max_tokens = self.llm_setting_widget.tokens_slider.value()
        selected_sys_msg = self.llm_setting_widget.sys_msg_input.toPlainText()
        selected_img_size = self.image_setting_widget.size_group.checkedButton().text() if self.image_setting_widget.size_group.checkedButton() else None
        selected_img_quality = self.image_setting_widget.quality_group.checkedButton().text() if self.image_setting_widget.quality_group.checkedButton() else None
        selected_img_num = self.image_setting_widget.img_num_slider.value()
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
        self.llm_setting_widget.selected_llm = self.llms_combobox.currentText()
        limits = self._get_limits_from_json()
        default_tokens = [4096, 1]
        max_tokens, max_temp = limits.get(self.llm_setting_widget.selected_llm, default_tokens)
        self._check_if_img()
        self.llm_setting_widget.check_if_reasoner()
        self.llm_setting_widget.tokens_slider.setMaximum(max_tokens)
        self.llm_setting_widget.max_tokens_lbl.setText(str(max_tokens))
        self.llm_setting_widget.temp_slider.setMaximum(20 if max_temp == 2 else 10)
        self.llm_setting_widget.max_temp_lbl.setText(str(max_temp))

    def _get_limits_from_json(self):
        models_data = FH.load_file("storage/assets/json/models.json")
        return {model_name: data["limits"] for model_name, data in models_data.items()} if models_data else {}

    def _check_if_img(self):
        if re.match(r"^DALL-E \d+", self.llm_setting_widget.selected_llm):
            self._show_img_settings()
        else:
            self._hide_img_settings()

        selected_size_button = self.image_setting_widget.size_group.checkedButton()
        if self.llm_setting_widget.selected_llm in ["DALL-E 2"]:
            self.image_setting_widget.img_num_w.show()
            self.image_setting_widget.checkbox_256x256.show()
            self.image_setting_widget.checkbox_512x512.show()
            self.image_setting_widget.checkbox_1024x1792.hide()
            self.image_setting_widget.checkbox_1792x1024.hide()
            self.image_setting_widget.img_quality_w.hide()
            if selected_size_button in [self.image_setting_widget.checkbox_1024x1792, self.image_setting_widget.checkbox_1792x1024]:
                self.image_setting_widget.checkbox_1024x1024.setChecked(True)

        elif self.llm_setting_widget.selected_llm in ["DALL-E 3"]:
            self.image_setting_widget.img_num_w.hide()
            self.image_setting_widget.checkbox_256x256.hide()
            self.image_setting_widget.checkbox_512x512.hide()
            self.image_setting_widget.checkbox_1024x1792.show()
            self.image_setting_widget.checkbox_1792x1024.show()
            self.image_setting_widget.checkbox_hd.show()
            if selected_size_button in [self.image_setting_widget.checkbox_256x256, self.image_setting_widget.checkbox_512x512]:
                self.image_setting_widget.checkbox_1024x1024.setChecked(True)

    def load_settings_from_json(self):
        """Load the saved settings from the JSON file and sets values"""
        settings = FH.load_file("storage/saved_settings.json")

        # Sets saved llm
        index = self.llms_combobox.findText(settings["llm_name"])
        if index != -1:
            self.llms_combobox.setCurrentIndex(index)
        # Sets temperature e max_tokens
        self.llm_setting_widget.temp_slider.setValue(int(settings["temperature"] * 10))
        self.llm_setting_widget.tokens_slider.setValue(int(settings["max_tokens"]))
        # Sets system_message
        self.llm_setting_widget.sys_msg_input.setText(settings["system_message"])
        # Sets reasoning_effort
        reasoning_effort = settings.get("reasoning_effort", "")
        for button in self.llm_setting_widget.reasoning_group.buttons():
            # Note: reasoning str is lowercase in the client
            if button.text() == reasoning_effort.capitalize():
                button.setChecked(True)
                break
        # Sets img_size
        img_size = settings.get("image_size", "")
        for button in self.image_setting_widget.size_group.buttons(): 
            if button.text() == img_size:
                button.setChecked(True)
                break
        # Sets img_quality
        img_quality = settings.get("image_quality", "")
        for button in self.image_setting_widget.quality_group.buttons(): 
            if button.text() == img_quality:
                button.setChecked(True)
                break
        # Update parameter limits based on the selected model
        self._change_needed_settings()

    def _on_settings_changed(self):
        """Connects settings widgets to send_new_settings_to_controller signal"""
        self.llms_combobox.currentIndexChanged.connect(self.send_new_settings_to_controller)
        self.llm_setting_widget.temp_slider.valueChanged.connect(self.send_new_settings_to_controller)
        self.llm_setting_widget.tokens_slider.valueChanged.connect(self.send_new_settings_to_controller)
        self.llm_setting_widget.sys_msg_input.textChanged.connect(self.send_new_settings_to_controller)
        self.image_setting_widget.size_group.buttonClicked.connect(self.send_new_settings_to_controller)
        self.llm_setting_widget.reasoning_group.buttonClicked.connect(self.send_new_settings_to_controller)
        self.image_setting_widget.quality_group.buttonClicked.connect(self.send_new_settings_to_controller)
        self.image_setting_widget.img_num_slider.valueChanged.connect(self.send_new_settings_to_controller)
