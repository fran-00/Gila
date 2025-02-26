import json

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
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


class ChangeSettings(QObject):
    new_settings_to_controller = Signal(str, float, int, str)

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
        self.on_llms_combobox()
        self.add_line_separator(self.change_settings_layout)
        self.on_temperature_slider()
        self.add_line_separator(self.change_settings_layout)
        self.on_max_tokens_slider()
        self.add_line_separator(self.change_settings_layout)
        self.on_system_message()
        self.llms_combobox.currentTextChanged.connect(self.update_sliders_values)
        self.on_settings_changed()
        self.load_settings_from_json()

    def on_settings_changed(self):
        """Connects settings widgets to send_new_settings_to_controller signal"""
        self.llms_combobox.currentIndexChanged.connect(self.send_new_settings_to_controller)
        self.temperature_slider.valueChanged.connect(self.send_new_settings_to_controller)
        self.tokens_slider.valueChanged.connect(self.send_new_settings_to_controller)
        self.system_message_input.textChanged.connect(self.send_new_settings_to_controller)

    def on_llms_combobox(self):
        """ Creates ComboBox with llms list """
        select_llm_label = QLabel("Model")
        select_llm_label.setAlignment(Qt.Alignment.AlignCenter)
        self.llms_combobox = QComboBox()
        for llm in self.current_settings.llms:
            self.llms_combobox.addItem(llm)
        self.llms_combobox.setCurrentIndex(-1)
        self.change_settings_layout.addWidget(select_llm_label)
        self.change_settings_layout.addWidget(self.llms_combobox)

    def on_temperature_slider(self):
        # Create widgets and slider's sub-layout
        select_temperature_label = QLabel("Temperature")
        select_temperature_label.setAlignment(Qt.Alignment.AlignCenter)
        temperature_slider_layout = QHBoxLayout()
        min_temperature_label = QLabel("0")
        self.max_temperature_label = QLabel("1")
        self.temperature_slider = QSlider(Qt.Horizontal)
        self.temperature_current_value_label = QLabel("0", objectName="temperature_current_value_label")
        # Adjust labels settings and width
        self.temperature_current_value_label.setAlignment(Qt.Alignment.AlignCenter)
        min_temperature_label.setAlignment(Qt.Alignment.AlignRight | Qt.Alignment.AlignVCenter)
        min_temperature_label.setFixedWidth(30)
        self.max_temperature_label.setFixedWidth(30)
        temperature_slider_layout.setStretchFactor(min_temperature_label, 0)
        temperature_slider_layout.setStretchFactor(self.temperature_slider, 1)
        temperature_slider_layout.setStretchFactor(self.max_temperature_label, 0)
        self.parent_class.window.assign_css_class(min_temperature_label, "slider_value_label")
        self.parent_class.window.assign_css_class(self.max_temperature_label, "slider_value_label")
        # Adjust slider's settings
        self.temperature_slider.setMinimum(0)
        self.temperature_slider.setMaximum(10)
        self.temperature_slider.setTickInterval(1)
        self.temperature_slider.setSingleStep(1)
        self.temperature_slider.valueChanged.connect(self.on_temperature_slider_changed)
        # Add widgets and slider's layout to modal's layout
        self.change_settings_layout.addWidget(select_temperature_label)
        temperature_slider_layout.addWidget(min_temperature_label)
        temperature_slider_layout.addWidget(self.temperature_slider)
        temperature_slider_layout.addWidget(self.max_temperature_label)
        self.change_settings_layout.addLayout(temperature_slider_layout)
        self.change_settings_layout.addWidget(self.temperature_current_value_label)

    def on_temperature_slider_changed(self):
        selected_temperature_value = self.temperature_slider.value() / 10
        self.temperature_current_value_label.setText(str(selected_temperature_value))

    def on_max_tokens_slider(self):
        """
        """
        # Create widgets and slider's sub-layout
        select_tokens_label = QLabel("Max Tokens")
        select_tokens_label.setAlignment(Qt.Alignment.AlignCenter)
        tokens_slider_layout = QHBoxLayout()
        min_tokens_label = QLabel("150")
        self.max_tokens_label = QLabel("4096")
        self.tokens_slider = QSlider(Qt.Horizontal)
        self.max_tokens_current_value_label = QLabel("1000", objectName="max_tokens_current_value_label")
        # Adjust labels settings and width
        self.max_tokens_current_value_label.setAlignment(Qt.Alignment.AlignCenter)
        min_tokens_label.setAlignment(Qt.Alignment.AlignRight | Qt.Alignment.AlignVCenter)
        min_tokens_label.setFixedWidth(30)
        self.max_tokens_label.setFixedWidth(30)
        tokens_slider_layout.setStretchFactor(min_tokens_label, 0)
        tokens_slider_layout.setStretchFactor(self.tokens_slider, 1)
        tokens_slider_layout.setStretchFactor(self.max_tokens_label, 0)
        self.parent_class.window.assign_css_class(min_tokens_label, "slider_value_label")
        self.parent_class.window.assign_css_class(self.max_tokens_label, "slider_value_label")
        # Adjust slider's settings
        self.tokens_slider.setMinimum(150)
        self.tokens_slider.setMaximum(4096)
        self.tokens_slider.setTickInterval(100)
        self.tokens_slider.setSingleStep(100)
        self.tokens_slider.valueChanged.connect(self.on_max_tokens_slider_changed)
        # Add widgets and slider's layout to modal's layout
        self.change_settings_layout.addWidget(select_tokens_label)
        tokens_slider_layout.addWidget(min_tokens_label)
        tokens_slider_layout.addWidget(self.tokens_slider)
        tokens_slider_layout.addWidget(self.max_tokens_label)
        self.change_settings_layout.addLayout(tokens_slider_layout)
        self.change_settings_layout.addWidget(self.max_tokens_current_value_label)

    def on_max_tokens_slider_changed(self):
        selected_max_tokens_value = self.tokens_slider.value()
        self.max_tokens_current_value_label.setText(str(selected_max_tokens_value))

    def on_system_message(self):
        system_message_label = QLabel("System Message")
        system_message_label.setAlignment(Qt.Alignment.AlignCenter)
        self.system_message_input = QTextEdit(objectName="system_message_widget")
        self.system_message_input.setMinimumSize(50, 50)
        system_message_layout = QVBoxLayout()
        system_message_layout.addWidget(system_message_label)
        system_message_layout.addWidget(self.system_message_input)
        self.change_settings_layout.addLayout(system_message_layout)

    def send_new_settings_to_controller(self):
        """ Sends new settings to controller: signal is triggered when
            Confirm Button is pressed
        """
        selected_llm = self.llms_combobox.currentText()
        selected_temperature = self.temperature_slider.value()
        selected_max_tokens = self.tokens_slider.value()
        selected_system_message = self.system_message_input.toPlainText()
        self.new_settings_to_controller.emit(
            selected_llm,
            selected_temperature,
            selected_max_tokens,
            selected_system_message
        )

    def update_sliders_values(self):
        """ Adjusts token limits and temperature range, based on a given model. """
        llm = self.llms_combobox.currentText()
        limits = {
            "GPT-4o mini": (16384, 2),
            "GPT-4o": (4096, 2),
            "GPT-4": (8192, 2),
            "GPT-4 Turbo": (4096, 2),
            "Gemini 2.0 Flash": (8192, 2),
            "Gemini 1.5 Flash": (8192, 2),
            "Gemini 1.5 Pro": (8192, 2),
            "DeepSeek-V3": (8192, 2),
            "DeepSeek-R1": (8192, 2),
            "Mistral Small": (8000, 1),
            "Pixtral": (8000, 1),
            "Command": (4000, 1),
            "Command R": (4000, 1),
            "Command R+": (4000, 1),
            "Llama70B": (8196, 1),
            "Qwen2.5-32B": (8000, 1),
            "Claude 3 Haiku": (4096, 1),
            "Claude 3 Opus": (4096, 1),
            "Claude 3 Sonnet": (4096, 1),
            "Claude 3.5 Sonnet": (8192, 1),
            "DALL-E-2": (0, 0),
            "DALL-E-3": (0, 0),
        }
        default_tokens = (4096, 2)
        max_tokens, max_temp = limits.get(llm, default_tokens)
        
        self.tokens_slider.setMaximum(max_tokens)
        self.max_tokens_label.setText(str(max_tokens))
        self.temperature_slider.setMaximum(20 if max_temp == 2 else 10)
        self.max_temperature_label.setText(str(max_temp))

    def add_line_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setMaximumHeight(1)
        self.parent_class.window.assign_css_class(line, "line_separator")
        layout.addWidget(line)

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
            # Update parameter limits based on the selected model
            self.update_sliders_values()

        except (FileNotFoundError, json.JSONDecodeError):
            return
