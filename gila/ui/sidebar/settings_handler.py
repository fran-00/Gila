import json

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


class SettingsHandler(QObject):
    new_settings_to_controller = Signal(str, float, int, str, str, str, int)

    def __init__(self, parent_class, current_settings):
        super().__init__()
        self.parent_class = parent_class
        self.current_settings = current_settings
        self.widget_container = QWidget(objectName="change_settings_widget")
        self.on_scroll_area()
        self.on_change_settings_layout()

    def on_scroll_area(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.widget_container)
        self.scroll_area.setWidgetResizable(True)

    def on_change_settings_layout(self):
        self.change_settings_layout = QVBoxLayout(self.widget_container)
        self.change_settings_layout.setAlignment(Qt.Alignment.AlignTop)
        self.on_llms_settings()
        self.add_line_separator(self.change_settings_layout)
        self.on_temperature_settings()
        self.on_image_size_settings()
        self.add_line_separator(self.change_settings_layout)
        self.on_max_tokens_settings()
        self.on_image_quality_settings()
        self.on_image_quantity_settings()
        self.add_line_separator(self.change_settings_layout)
        self.on_system_message_settings()
        self.llms_combobox.currentTextChanged.connect(self.change_needed_settings)
        self.on_settings_changed()
        self.load_settings_from_json()

        self.check_if_image()

    def on_llms_settings(self):
        """ Creates ComboBox with llms list """
        select_llm_label = QLabel("Model")
        self.parent_class.window.assign_css_class(select_llm_label, "setting_name")
        select_llm_label.setAlignment(Qt.Alignment.AlignCenter)
        self.llms_combobox = QComboBox()
        for llm in self.current_settings.llms:
            self.llms_combobox.addItem(llm)
        self.llms_combobox.setCurrentIndex(-1)
        self.change_settings_layout.addWidget(select_llm_label)
        self.change_settings_layout.addWidget(self.llms_combobox)

    def on_temperature_settings(self):
        """ Widget to adjust temperature settings """
        # Create inner widget and layout to contain temperature settings
        self.temperature_inner_widget = QWidget()
        temperature_inner_layout = QVBoxLayout(self.temperature_inner_widget)
        temperature_inner_layout.setContentsMargins(0, 0, 0, 0)
        # Create temperature label
        select_temperature_label = QLabel("Temperature")
        self.parent_class.window.assign_css_class(select_temperature_label, "setting_name")
        select_temperature_label.setAlignment(Qt.Alignment.AlignCenter)
        # Create widgets and slider's sub-layout
        temperature_slider_sub_layout = QHBoxLayout()
        min_temperature_label = QLabel("0")
        self.max_temperature_label = QLabel("1")
        self.temperature_slider = QSlider(Qt.Horizontal)
        self.temperature_current_value_label = QLabel("0")
        self.parent_class.window.assign_css_class(self.temperature_current_value_label, "current_value_label")
        # Adjust labels settings and width
        self.temperature_current_value_label.setAlignment(Qt.Alignment.AlignCenter)
        min_temperature_label.setAlignment(Qt.Alignment.AlignRight | Qt.Alignment.AlignVCenter)
        min_temperature_label.setFixedWidth(30)
        self.max_temperature_label.setFixedWidth(30)
        temperature_slider_sub_layout.setStretchFactor(min_temperature_label, 0)
        temperature_slider_sub_layout.setStretchFactor(self.temperature_slider, 1)
        temperature_slider_sub_layout.setStretchFactor(self.max_temperature_label, 0)
        self.parent_class.window.assign_css_class(min_temperature_label, "slider_value_label")
        self.parent_class.window.assign_css_class(self.max_temperature_label, "slider_value_label")
        # Adjust slider's settings
        self.temperature_slider.setMinimum(0)
        self.temperature_slider.setMaximum(10)
        self.temperature_slider.setTickInterval(1)
        self.temperature_slider.setSingleStep(1)
        self.temperature_slider.valueChanged.connect(self.on_temperature_settings_changed)
        # Add widgets and slider to temperature slider sub layout
        temperature_slider_sub_layout.addWidget(min_temperature_label)
        temperature_slider_sub_layout.addWidget(self.temperature_slider)
        temperature_slider_sub_layout.addWidget(self.max_temperature_label)
        # Add label, slider sub layout and current value to temperature inner layout
        temperature_inner_layout.addWidget(select_temperature_label)
        temperature_inner_layout.addLayout(temperature_slider_sub_layout)
        temperature_inner_layout.addWidget(self.temperature_current_value_label)
        # Add temperture inner widget to main layout
        self.change_settings_layout.addWidget(self.temperature_inner_widget)

    def on_temperature_settings_changed(self):
        selected_temperature_value = self.temperature_slider.value() / 10
        self.temperature_current_value_label.setText(str(selected_temperature_value))

    def on_max_tokens_settings(self):
        """ Widget to adjust max tokens settings """
        # Create inner widget and layout to contain max tokens settings
        self.max_tokens_inner_widget = QWidget()
        max_tokens_inner_layout = QVBoxLayout(self.max_tokens_inner_widget)
        max_tokens_inner_layout.setContentsMargins(0, 0, 0, 0)
        # Create max_tokens label
        select_tokens_label = QLabel("Max Tokens")
        self.parent_class.window.assign_css_class(select_tokens_label, "setting_name")
        select_tokens_label.setAlignment(Qt.Alignment.AlignCenter)
        # Create widgets and slider's sub-layout
        tokens_slider_sub_layout = QHBoxLayout()
        min_tokens_label = QLabel("150")
        self.max_tokens_label = QLabel("4096")
        self.tokens_slider = QSlider(Qt.Horizontal)
        self.max_tokens_current_value_label = QLabel("1000")
        self.parent_class.window.assign_css_class(self.max_tokens_current_value_label, "current_value_label")
        # Adjust labels settings and width
        self.max_tokens_current_value_label.setAlignment(Qt.Alignment.AlignCenter)
        min_tokens_label.setAlignment(Qt.Alignment.AlignRight | Qt.Alignment.AlignVCenter)
        min_tokens_label.setFixedWidth(30)
        self.max_tokens_label.setFixedWidth(30)
        tokens_slider_sub_layout.setStretchFactor(min_tokens_label, 0)
        tokens_slider_sub_layout.setStretchFactor(self.tokens_slider, 1)
        tokens_slider_sub_layout.setStretchFactor(self.max_tokens_label, 0)
        self.parent_class.window.assign_css_class(min_tokens_label, "slider_value_label")
        self.parent_class.window.assign_css_class(self.max_tokens_label, "slider_value_label")
        # Adjust slider's settings
        self.tokens_slider.setMinimum(150)
        self.tokens_slider.setMaximum(4096)
        self.tokens_slider.setTickInterval(100)
        self.tokens_slider.setSingleStep(100)
        self.tokens_slider.valueChanged.connect(self.on_max_tokens_settings_changed)
        # Add widgets and slider to max_tokens slider sub layout
        tokens_slider_sub_layout.addWidget(min_tokens_label)
        tokens_slider_sub_layout.addWidget(self.tokens_slider)
        tokens_slider_sub_layout.addWidget(self.max_tokens_label)
        # Add label, slider sub layout and current value to max tokens inner layout
        max_tokens_inner_layout.addWidget(select_tokens_label)
        max_tokens_inner_layout.addLayout(tokens_slider_sub_layout)
        max_tokens_inner_layout.addWidget(self.max_tokens_current_value_label)
        # Add temperture inner widget to main layout
        self.change_settings_layout.addWidget(self.max_tokens_inner_widget)

    def on_max_tokens_settings_changed(self):
        selected_max_tokens_value = self.tokens_slider.value()
        self.max_tokens_current_value_label.setText(str(selected_max_tokens_value))

    def on_system_message_settings(self):
        """ Widget to adjust system message setting """
        # Create inner widget and layout to contain system message
        self.system_message_inner_widget = QWidget()
        system_message_inner_layout = QVBoxLayout(self.system_message_inner_widget)
        system_message_inner_layout.setContentsMargins(0, 0, 0, 0)
        # Create system message label
        system_message_label = QLabel("System Message")
        self.parent_class.window.assign_css_class(system_message_label, "setting_name")
        system_message_label.setAlignment(Qt.Alignment.AlignCenter)
        # Create system message QTextEdit
        self.system_message_input = QTextEdit(objectName="system_message_widget")
        # Add label and QTextEdit widget to system message inner layout
        system_message_inner_layout.addWidget(system_message_label)
        system_message_inner_layout.addWidget(self.system_message_input)
        # Add system message inner widget to main layout
        self.change_settings_layout.addWidget(self.system_message_inner_widget)

    def on_image_size_settings(self):
        """ Widget to adjust image size settings """
        # Create inner widget and layout to contain image size settings
        self.image_size_inner_widget = QWidget()
        image_size_inner_layout = QVBoxLayout(self.image_size_inner_widget)
        image_size_inner_layout.setContentsMargins(0, 0, 0, 0)
        # Create image size label
        select_image_size_label = QLabel("Image Size")
        self.parent_class.window.assign_css_class(select_image_size_label, "setting_name")
        select_image_size_label.setAlignment(Qt.Alignment.AlignCenter)
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
        # Add label and checkboxes to image size inner layout
        image_size_inner_layout.addWidget(select_image_size_label)
        image_size_inner_layout.addWidget(self.checkbox_256x256)
        image_size_inner_layout.addWidget(self.checkbox_512x512)
        image_size_inner_layout.addWidget(self.checkbox_1024x1024)
        image_size_inner_layout.addWidget(self.checkbox_1024x1792)
        image_size_inner_layout.addWidget(self.checkbox_1792x1024)
        # Add image size inner widget to main layout
        self.change_settings_layout.addWidget(self.image_size_inner_widget)

    def on_image_quality_settings(self):
        """ Widget to adjust image quality settings """
        # Create inner widget and layout to contain image quality settings
        self.image_quality_inner_widget = QWidget()
        image_quality_inner_layout = QVBoxLayout(self.image_quality_inner_widget)
        image_quality_inner_layout.setContentsMargins(0, 0, 0, 0)
        # Create image quality label
        select_image_quality_label = QLabel("Image Quality")
        self.parent_class.window.assign_css_class(select_image_quality_label, "setting_name")
        select_image_quality_label.setAlignment(Qt.Alignment.AlignCenter)
        # Create widget's button group with checkboxes
        self.quality_group = QButtonGroup(self)
        self.quality_group.setExclusive(True)
        self.checkbox_standard = QCheckBox("Standard")
        self.checkbox_hd = QCheckBox("HD")
        self.quality_group.addButton(self.checkbox_standard)
        self.quality_group.addButton(self.checkbox_hd)
        # Add label and checkboxes to image quality inner layout
        image_quality_inner_layout.addWidget(select_image_quality_label)
        image_quality_inner_layout.addWidget(self.checkbox_standard)
        image_quality_inner_layout.addWidget(self.checkbox_hd)
        # Add image quality inner widget to main layout
        self.change_settings_layout.addWidget(self.image_quality_inner_widget)

    def on_image_quantity_settings(self):
        """ Widget to adjust image quantity settings """
        # Create inner widget and layout to contain max tokens settings
        self.image_quantity_inner_widget = QWidget()
        image_quantity_inner_layout = QVBoxLayout(self.image_quantity_inner_widget)
        image_quantity_inner_layout.setContentsMargins(0, 0, 0, 0)
        # Create max_tokens label
        select_image_quantity_label = QLabel("Number of images")
        self.parent_class.window.assign_css_class(select_image_quantity_label, "setting_name")
        select_image_quantity_label.setAlignment(Qt.Alignment.AlignCenter)
        # Create widgets and slider's sub-layout
        image_quantity_slider_sub_layout = QHBoxLayout()
        min_image_quantity_label = QLabel("1")
        max_image_quantity_label = QLabel("10")
        self.image_quantity_slider = QSlider(Qt.Horizontal)
        self.max_image_quantity_current_value_label = QLabel("1")
        self.parent_class.window.assign_css_class(self.max_image_quantity_current_value_label, "current_value_label")
        # Adjust labels settings and width
        self.max_image_quantity_current_value_label.setAlignment(Qt.Alignment.AlignCenter)
        min_image_quantity_label.setAlignment(Qt.Alignment.AlignRight | Qt.Alignment.AlignVCenter)
        min_image_quantity_label.setFixedWidth(30)
        max_image_quantity_label.setFixedWidth(30)
        image_quantity_slider_sub_layout.setStretchFactor(min_image_quantity_label, 0)
        image_quantity_slider_sub_layout.setStretchFactor(self.image_quantity_slider, 1)
        image_quantity_slider_sub_layout.setStretchFactor(max_image_quantity_label, 0)
        self.parent_class.window.assign_css_class(min_image_quantity_label, "slider_value_label")
        self.parent_class.window.assign_css_class(max_image_quantity_label, "slider_value_label")
        # Adjust slider's settings
        self.image_quantity_slider.setMinimum(1)
        self.image_quantity_slider.setMaximum(10)
        self.image_quantity_slider.setTickInterval(1)
        self.image_quantity_slider.setSingleStep(1)
        self.image_quantity_slider.valueChanged.connect(self.on_image_quantity_settings_changed)
        # Add widgets and slider to image quantity slider sub layout
        image_quantity_slider_sub_layout.addWidget(min_image_quantity_label)
        image_quantity_slider_sub_layout.addWidget(self.image_quantity_slider)
        image_quantity_slider_sub_layout.addWidget(max_image_quantity_label)
        # Add label, slider sub layout and current value to max tokens inner layout
        image_quantity_inner_layout.addWidget(select_image_quantity_label)
        image_quantity_inner_layout.addLayout(image_quantity_slider_sub_layout)
        image_quantity_inner_layout.addWidget(self.max_image_quantity_current_value_label)
        # Add temperture inner widget to main layout
        self.change_settings_layout.addWidget(self.image_quantity_inner_widget)

    def on_image_quantity_settings_changed(self):
        self.max_image_quantity_current_value_label.setText(str(self.image_quantity_slider.value()))

    def add_line_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setMaximumHeight(1)
        self.parent_class.window.assign_css_class(line, "line_separator")
        layout.addWidget(line)

    def on_show_image_settings(self):
        self.image_size_inner_widget.show()
        self.image_quality_inner_widget.show()
        self.image_quantity_inner_widget.show()
        self.temperature_inner_widget.hide()
        self.max_tokens_inner_widget.hide()
        self.system_message_inner_widget.hide()

    def on_hide_image_settings(self):
        self.image_size_inner_widget.hide()
        self.image_quality_inner_widget.hide()
        self.image_quantity_inner_widget.hide()
        self.temperature_inner_widget.show()
        self.max_tokens_inner_widget.show()
        self.system_message_inner_widget.show()

    def send_new_settings_to_controller(self):
        """ Sends new settings to controller: signal is triggered when
            Confirm Button is pressed
        """
        selected_llm = self.llms_combobox.currentText()
        selected_temperature = self.temperature_slider.value()
        selected_max_tokens = self.tokens_slider.value()
        selected_system_message = self.system_message_input.toPlainText()
        selected_image_size = self.size_group.checkedButton().text() if self.size_group.checkedButton() else None
        selected_image_quality = self.quality_group.checkedButton().text() if self.quality_group.checkedButton() else None
        selected_image_quantity = self.image_quantity_slider.value()
        self.new_settings_to_controller.emit(
            selected_llm,
            selected_temperature,
            selected_max_tokens,
            selected_system_message,
            selected_image_size,
            selected_image_quality,
            selected_image_quantity
        )

    def change_needed_settings(self):
        """ Adjusts token limits and temperature range, based on a given model. """
        self.selected_llm = self.llms_combobox.currentText()
        limits = {
            "GPT-4o mini": (16384, 2),
            "GPT-4o": (4096, 2),
            "GPT-4": (8192, 2),
            "GPT-4 Turbo": (4096, 2),
            "GPT-4.5 preview": (16384, 2),
            "Gemini 2.0 Flash": (8192, 2),
            "Gemini 1.5 Flash": (8192, 2),
            "Gemini 1.5 Pro": (8192, 2),
            "DeepSeek-V3": (8192, 2),
            "DeepSeek-R1": (8192, 2),
            "Mistral Small": (131000, 1),
            "Pixtral": (8000, 1),
            "Mistral Nemo": (8000, 1),
            "Codestral Mamba": (256000, 1),
            "Command": (4000, 1),
            "Command R": (4000, 1),
            "Command R+": (4000, 1),
            "Llama70B": (8196, 1),
            "Qwen2.5-32B": (8000, 1),
            "Claude 3 Haiku": (4096, 1),
            "Claude 3 Opus": (4096, 1),
            "Claude 3 Sonnet": (4096, 1),
            "Claude 3.5 Sonnet": (8192, 1),
            # WARNING, they must values supported by other models!
            "DALL-E 2": (4096, 1),
            "DALL-E 3": (4096, 1),
        }
        default_tokens = (4096, 1)
        max_tokens, max_temp = limits.get(self.selected_llm, default_tokens)
        self.check_if_image()
        self.tokens_slider.setMaximum(max_tokens)
        self.max_tokens_label.setText(str(max_tokens))
        self.temperature_slider.setMaximum(20 if max_temp == 2 else 10)
        self.max_temperature_label.setText(str(max_temp))

    def check_if_image(self):
        if self.selected_llm in ["DALL-E 2", "DALL-E 3"]:
            self.on_show_image_settings()
        else:
            self.on_hide_image_settings()

        selected_size_button = self.size_group.checkedButton()
        if self.selected_llm in ["DALL-E 2"]:
            self.image_quantity_inner_widget.show()
            self.checkbox_256x256.show()
            self.checkbox_512x512.show()
            self.checkbox_1024x1792.hide()
            self.checkbox_1792x1024.hide()
            self.image_quality_inner_widget.hide()
            if selected_size_button in [self.checkbox_1024x1792, self.checkbox_1792x1024]:
                self.checkbox_1024x1024.setChecked(True)

        elif self.selected_llm in ["DALL-E 3"]:
            self.image_quantity_inner_widget.hide()
            self.checkbox_256x256.hide()
            self.checkbox_512x512.hide()
            self.checkbox_1024x1792.show()
            self.checkbox_1792x1024.show()
            self.checkbox_hd.show()
            if selected_size_button in [self.checkbox_256x256, self.checkbox_512x512]:
                self.checkbox_1024x1024.setChecked(True)

    def load_settings_from_json(self):
        """Loads the saved settings from the JSON file and sets values"""
        try:
            with open("storage/saved_settings.json", "r") as file:
                settings = json.load(file)

            # Sets saved llm
            index = self.llms_combobox.findText(settings["llm_name"])
            if index != -1:
                self.llms_combobox.setCurrentIndex(index)
            # Sets temperature e max_tokens
            self.temperature_slider.setValue(int(settings["temperature"] * 10))
            self.tokens_slider.setValue(int(settings["max_tokens"]))
            # # Sets system_message
            self.system_message_input.setText(settings["system_message"])

            image_size = settings.get("image_size", "")
            for button in self.size_group.buttons(): 
                if button.text() == image_size:
                    button.setChecked(True)
                    break
            image_quality = settings.get("image_quality", "")
            for button in self.quality_group.buttons(): 
                if button.text() == image_quality:
                    button.setChecked(True)
                    break
            # Update parameter limits based on the selected model
            self.change_needed_settings()

        except (FileNotFoundError, json.JSONDecodeError):
            return

    def on_settings_changed(self):
        """Connects settings widgets to send_new_settings_to_controller signal"""
        self.llms_combobox.currentIndexChanged.connect(self.send_new_settings_to_controller)
        self.temperature_slider.valueChanged.connect(self.send_new_settings_to_controller)
        self.tokens_slider.valueChanged.connect(self.send_new_settings_to_controller)
        self.system_message_input.textChanged.connect(self.send_new_settings_to_controller)
        self.size_group.buttonClicked.connect(self.send_new_settings_to_controller)
        self.quality_group.buttonClicked.connect(self.send_new_settings_to_controller)
        self.image_quantity_slider.valueChanged.connect(self.send_new_settings_to_controller)
