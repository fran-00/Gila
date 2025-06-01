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

    def __init__(self, parent_class, current_settings):
        super().__init__()
        self.parent_class = parent_class
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

    def _build_llms_settings(self):
        """ Creates ComboBox with llms list """
        select_llm_lbl = QLabel("Model")
        self.parent_class.window.assign_css_class(select_llm_lbl, "setting_name")
        select_llm_lbl.setAlignment(Qt.Alignment.AlignCenter)
        self.llms_combobox = QComboBox()
        for llm in self.current_settings.llms:
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
        self.parent_class.window.assign_css_class(temp_lbl, "setting_name")
        temp_lbl.setAlignment(Qt.Alignment.AlignCenter)
        # Create widgets and slider's sub-layout
        temp_slider_sub_h = QHBoxLayout()
        min_temp_lbl = QLabel("0")
        self.max_temp_lbl = QLabel("1")
        self.temp_slider = QSlider(Qt.Horizontal)
        self.current_temp_lbl = QLabel("0")
        self.parent_class.window.assign_css_class(self.current_temp_lbl, "current_value_lbl")
        # Adjust lbls settings and width
        self.current_temp_lbl.setAlignment(Qt.Alignment.AlignCenter)
        min_temp_lbl.setAlignment(Qt.Alignment.AlignRight | Qt.Alignment.AlignVCenter)
        min_temp_lbl.setFixedWidth(30)
        self.max_temp_lbl.setFixedWidth(30)
        temp_slider_sub_h.setStretchFactor(min_temp_lbl, 0)
        temp_slider_sub_h.setStretchFactor(self.temp_slider, 1)
        temp_slider_sub_h.setStretchFactor(self.max_temp_lbl, 0)
        self.parent_class.window.assign_css_class(min_temp_lbl, "slider_value_lbl")
        self.parent_class.window.assign_css_class(self.max_temp_lbl, "slider_value_lbl")
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
        self.parent_class.window.assign_css_class(self.select_tokens_lbl, "setting_name")
        self.select_tokens_lbl.setAlignment(Qt.Alignment.AlignCenter)
        # Create widgets and slider's sub-layout
        tokens_slider_sub_h = QHBoxLayout()
        min_tokens_lbl = QLabel("150")
        self.max_tokens_lbl = QLabel("4096")
        self.tokens_slider = QSlider(Qt.Horizontal)
        self.max_tokens_current_value_lbl = QLabel("1000")
        self.parent_class.window.assign_css_class(self.max_tokens_current_value_lbl, "current_value_lbl")
        # Adjust labels settings and width
        self.max_tokens_current_value_lbl.setAlignment(Qt.Alignment.AlignCenter)
        min_tokens_lbl.setAlignment(Qt.Alignment.AlignRight | Qt.Alignment.AlignVCenter)
        min_tokens_lbl.setFixedWidth(30)
        self.max_tokens_lbl.setFixedWidth(30)
        tokens_slider_sub_h.setStretchFactor(min_tokens_lbl, 0)
        tokens_slider_sub_h.setStretchFactor(self.tokens_slider, 1)
        tokens_slider_sub_h.setStretchFactor(self.max_tokens_lbl, 0)
        self.parent_class.window.assign_css_class(min_tokens_lbl, "slider_value_lbl")
        self.parent_class.window.assign_css_class(self.max_tokens_lbl, "slider_value_lbl")
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
        self.parent_class.window.assign_css_class(sys_msg_lbl, "setting_name")
        sys_msg_lbl.setAlignment(Qt.Alignment.AlignCenter)
        # Create system message QTextEdit
        self.sys_msg_input = QTextEdit(objectName="sys_msg_widget")
        # Add lbl and QTextEdit widget to system message inner layout
        box_v.addWidget(sys_msg_lbl)
        box_v.addWidget(self.sys_msg_input)
        # Add system message inner widget to main layout
        self.layout.addWidget(self.sys_msg_w)

    def _build_img_size_settings(self):
        """ Widget to adjust img size settings """
        # Create inner widget and layout to contain img size settings
        self.img_size_w = QWidget()
        box_v = QVBoxLayout(self.img_size_w)
        box_v.setContentsMargins(0, 0, 0, 0)
        # Create img size lbl
        select_img_size_lbl = QLabel("Image Size")
        self.parent_class.window.assign_css_class(select_img_size_lbl, "setting_name")
        select_img_size_lbl.setAlignment(Qt.Alignment.AlignCenter)
        # Create widget's button group with all checkboxes
        self.size_group = QButtonGroup(self)
        self.size_group.setExclusive(True)  
        self.checkbox_256x256 = QCheckBox("256x256")
        self.checkbox_512x512 = QCheckBox("512x512")
        self.checkbox_1024x1024 = QCheckBox("1024x1024")
        self.checkbox_1024x1792 = QCheckBox("1024x1792")
        self.checkbox_1792x1024 = QCheckBox("1792x1024")
        self.size_group.addButton(self.checkbox_256x256)
        self.size_group.addButton(self.checkbox_512x512)
        self.size_group.addButton(self.checkbox_1024x1024)
        self.size_group.addButton(self.checkbox_1024x1792)
        self.size_group.addButton(self.checkbox_1792x1024)
        # Add lbl and checkboxes to img size inner layout
        box_v.addWidget(select_img_size_lbl)
        box_v.addWidget(self.checkbox_256x256)
        box_v.addWidget(self.checkbox_512x512)
        box_v.addWidget(self.checkbox_1024x1024)
        box_v.addWidget(self.checkbox_1024x1792)
        box_v.addWidget(self.checkbox_1792x1024)
        # Add img size inner widget to main layout
        self.layout.addWidget(self.img_size_w)

    def _build_img_quality_settings(self):
        """ Widget to adjust img quality settings """
        # Create inner widget and layout to contain img quality settings
        self.img_quality_w = QWidget()
        box_v = QVBoxLayout(self.img_quality_w)
        box_v.setContentsMargins(0, 0, 0, 0)
        # Create img quality lbl
        select_img_quality_lbl = QLabel("Image Quality")
        self.parent_class.window.assign_css_class(select_img_quality_lbl, "setting_name")
        select_img_quality_lbl.setAlignment(Qt.Alignment.AlignCenter)
        # Create widget's button group with checkboxes
        self.quality_group = QButtonGroup(self)
        self.quality_group.setExclusive(True)
        self.checkbox_standard = QCheckBox("Standard")
        self.checkbox_hd = QCheckBox("HD")
        self.quality_group.addButton(self.checkbox_standard)
        self.quality_group.addButton(self.checkbox_hd)
        # Add lbl and checkboxes to img quality inner layout
        box_v.addWidget(select_img_quality_lbl)
        box_v.addWidget(self.checkbox_standard)
        box_v.addWidget(self.checkbox_hd)
        # Add img quality inner widget to main layout
        self.layout.addWidget(self.img_quality_w)

    def _build_img_num_settings(self):
        """ Widget to adjust img quantity settings """
        # Create inner widget and layout to contain max tokens settings
        self.img_num_w = QWidget()
        box_v = QVBoxLayout(self.img_num_w)
        box_v.setContentsMargins(0, 0, 0, 0)
        # Create max_tokens lbl
        select_img_num_lbl = QLabel("Number of images")
        self.parent_class.window.assign_css_class(select_img_num_lbl, "setting_name")
        select_img_num_lbl.setAlignment(Qt.Alignment.AlignCenter)
        # Create widgets and slider's sub-layout
        img_num_slider_sub_h = QHBoxLayout()
        min_img_num_lbl = QLabel("1")
        max_img_num_lbl = QLabel("10")
        self.img_num_slider = QSlider(Qt.Horizontal)
        self.max_img_num_current_value_lbl = QLabel("1")
        self.parent_class.window.assign_css_class(self.max_img_num_current_value_lbl, "current_value_lbl")
        # Adjust lbls settings and width
        self.max_img_num_current_value_lbl.setAlignment(Qt.Alignment.AlignCenter)
        min_img_num_lbl.setAlignment(Qt.Alignment.AlignRight | Qt.Alignment.AlignVCenter)
        min_img_num_lbl.setFixedWidth(30)
        max_img_num_lbl.setFixedWidth(30)
        img_num_slider_sub_h.setStretchFactor(min_img_num_lbl, 0)
        img_num_slider_sub_h.setStretchFactor(self.img_num_slider, 1)
        img_num_slider_sub_h.setStretchFactor(max_img_num_lbl, 0)
        self.parent_class.window.assign_css_class(min_img_num_lbl, "slider_value_lbl")
        self.parent_class.window.assign_css_class(max_img_num_lbl, "slider_value_lbl")
        # Adjust slider's settings
        self.img_num_slider.setMinimum(1)
        self.img_num_slider.setMaximum(10)
        self.img_num_slider.setTickInterval(1)
        self.img_num_slider.setSingleStep(1)
        self.img_num_slider.valueChanged.connect(self._on_img_num_settings_changed)
        # Add widgets and slider to img quantity slider sub layout
        img_num_slider_sub_h.addWidget(min_img_num_lbl)
        img_num_slider_sub_h.addWidget(self.img_num_slider)
        img_num_slider_sub_h.addWidget(max_img_num_lbl)
        # Add lbl, slider sub layout and current value to max tokens inner layout
        box_v.addWidget(select_img_num_lbl)
        box_v.addLayout(img_num_slider_sub_h)
        box_v.addWidget(self.max_img_num_current_value_lbl)
        # Add temperture inner widget to main layout
        self.layout.addWidget(self.img_num_w)

    def _on_img_num_settings_changed(self):
        self.max_img_num_current_value_lbl.setText(str(self.img_num_slider.value()))

    def _build_reasoning_settings(self):
        """ Widget to adjust reasoning effort settings """
        # Create inner widget and layout to contain reasoning effort settings
        self.reasoning_w = QWidget()
        box_v = QVBoxLayout(self.reasoning_w)
        box_v.setContentsMargins(0, 0, 0, 0)
        # Create reasoning effort lbl
        select_reasoning_lbl = QLabel("Reasoning Effort")
        self.parent_class.window.assign_css_class(select_reasoning_lbl, "setting_name")
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

    def add_line_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setMaximumHeight(1)
        self.parent_class.window.assign_css_class(line, "line_separator")
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
