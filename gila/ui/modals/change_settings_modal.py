from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
                               QPushButton, QSlider, QFrame)

from .parent_modal import Modal


class ChangeSettingsModal(Modal):
    new_settings_to_controller = Signal(str, float, int)

    def __init__(self, window, current_settings):
        super().__init__(window)
        self.setWindowTitle("Change Settings")
        self.current_settings = current_settings
        self.on_modal_layout()

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.on_modal_text()
        self.modal_text.setText("Change settings, they will be applied when starting a new chat.")
        self.add_line_separator(self.modal_layout)
        self.on_llms_combobox()
        self.add_line_separator(self.modal_layout)
        self.on_temperature_slider()
        self.add_line_separator(self.modal_layout)
        self.on_max_tokens_slider()
        self.on_confirm_button()
        self.llms_combobox.currentTextChanged.connect(self.update_sliders_values)

    def on_llms_combobox(self):
        """ Creates ComboBox with llms list """
        select_llm_label = QLabel("Model")
        self.llms_combobox = QComboBox()
        for llm in self.current_settings.llms:
            self.llms_combobox.addItem(llm)
        self.modal_layout.addWidget(select_llm_label)
        self.modal_layout.addWidget(self.llms_combobox)

    def on_temperature_slider(self):
        # Create widgets and slider's sub-layout
        select_temperature_label = QLabel("Temperature")
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
        self.window.assign_css_class(min_temperature_label, "slider_value_label")
        self.window.assign_css_class(self.max_temperature_label, "slider_value_label")
        # Adjust slider's settings
        self.temperature_slider.setMinimum(0)
        self.temperature_slider.setMaximum(10)
        self.temperature_slider.setTickInterval(1)
        self.temperature_slider.setSingleStep(1)
        self.temperature_slider.valueChanged.connect(self.on_temperature_slider_changed)
        # Add widgets and slider's layout to modal's layout
        self.modal_layout.addWidget(select_temperature_label)
        temperature_slider_layout.addWidget(min_temperature_label)
        temperature_slider_layout.addWidget(self.temperature_slider)
        temperature_slider_layout.addWidget(self.max_temperature_label)
        self.modal_layout.addLayout(temperature_slider_layout)
        self.modal_layout.addWidget(self.temperature_current_value_label)

    def on_temperature_slider_changed(self):
        selected_temperature_value = self.temperature_slider.value() / 10
        self.temperature_current_value_label.setText(str(selected_temperature_value))

    def update_current_settings(self, settings):
        self.temperature_slider.setValue(int(settings[3]) * 10)
        self.tokens_slider.setValue(int(settings[4]))

    def on_max_tokens_slider(self):
        """
        Forse imposto molto lunga, lunga, media e corta e assegno un valore ai veri
        estremi direttamente nel client
        """
        # Create widgets and slider's sub-layout
        select_tokens_label = QLabel("Max Tokens")
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
        self.window.assign_css_class(min_tokens_label, "slider_value_label")
        self.window.assign_css_class(self.max_tokens_label, "slider_value_label")
        # Adjust slider's settings
        self.tokens_slider.setMinimum(150)
        self.tokens_slider.setMaximum(4096)
        self.tokens_slider.setTickInterval(100)
        self.tokens_slider.setSingleStep(100)
        self.tokens_slider.valueChanged.connect(self.on_max_tokens_slider_changed)
        # Add widgets and slider's layout to modal's layout
        self.modal_layout.addWidget(select_tokens_label)
        tokens_slider_layout.addWidget(min_tokens_label)
        tokens_slider_layout.addWidget(self.tokens_slider)
        tokens_slider_layout.addWidget(self.max_tokens_label)
        self.modal_layout.addLayout(tokens_slider_layout)
        self.modal_layout.addWidget(self.max_tokens_current_value_label)

    def on_max_tokens_slider_changed(self):
        selected_max_tokens_value = self.tokens_slider.value()
        self.max_tokens_current_value_label.setText(str(selected_max_tokens_value))

    def on_confirm_button(self):
        """ Creates button to confirm llm selection """
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.send_new_settings_to_controller)
        confirm_button.clicked.connect(self.accept)
        self.modal_layout.addWidget(confirm_button)

    def send_new_settings_to_controller(self):
        """ Sends new settings to controller: signal is triggered when
            Confirm Button is pressed
        """
        selected_llm = self.llms_combobox.currentText()
        selected_temperature = self.temperature_slider.value()
        selected_max_tokens = self.tokens_slider.value()
        self.new_settings_to_controller.emit(selected_llm, selected_temperature, selected_max_tokens)

    def update_sliders_values(self):
        """ Adjusts token limits and temperature range, based on a given model. """
        llm = self.llms_combobox.currentText()
        limits = {
            "GPT-4o mini": (16384, 2),
            "GPT-4o": (4096, 2),
            "GPT-4 Turbo": (4096, 2),
            "GPT-4": (8192, 2),
            "Gemini 1.5 Flash": (8192, 2),
            "Gemini 1.5 Pro": (8192, 2),
            "Command": (4000, 1),
            "Command R": (4000, 1),
            "Command R+": (4000, 1),
        }
        default_tokens = (4096, 2)
        max_tokens, max_temp = limits.get(llm, default_tokens)
        
        self.tokens_slider.setMaximum(max_tokens)
        self.max_tokens_label.setText(str(max_tokens))
        self.temperature_slider.setMaximum(20 if max_temp == 2 else 10)
        self.max_temperature_label.setText(str(max_temp))