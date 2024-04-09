from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
                               QPushButton, QSlider, QFrame)

from .parent_modal import Modal


class ChangeSettingsModal(Modal):
    new_settings_to_controller = Signal(str, float, int)

    def __init__(self, window, current_settings):
        super().__init__(window)
        self.setWindowTitle("Modifica Impostazioni")
        self.current_settings = current_settings
        self.on_modal_layout()

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.on_modal_text()
        self.modal_text.setText("Modifica le impostazioni, saranno applicate all'avvio di una nuova chat.")
        self.add_line_separator(self.modal_layout)
        self.on_llms_combobox()
        self.add_line_separator(self.modal_layout)
        self.on_temperature_slider()
        self.add_line_separator(self.modal_layout)
        self.on_max_tokens_slider()
        self.on_confirm_button()

    def on_llms_combobox(self):
        """ Creates ComboBox with llms list """
        select_llm_label = QLabel("Modello")
        self.llms_combobox = QComboBox()
        for llm in self.current_settings.llms:
            self.llms_combobox.addItem(llm)
        self.modal_layout.addWidget(select_llm_label)
        self.modal_layout.addWidget(self.llms_combobox)

    def on_temperature_slider(self):
        # Create widgets and slider's sub-layout
        select_temperature_label = QLabel("Temperatura")
        temperature_slider_layout = QHBoxLayout()
        min_temperature_label = QLabel("0")
        max_temperature_label = QLabel("2")
        self.temperature_slider = QSlider(Qt.Horizontal)
        self.temperature_current_value_label = QLabel("0", objectName="temperature_current_value_label")
        # Adjust labels settings and width
        self.temperature_current_value_label.setAlignment(Qt.Alignment.AlignCenter)
        min_temperature_label.setAlignment(Qt.Alignment.AlignRight | Qt.Alignment.AlignVCenter)
        min_temperature_label.setFixedWidth(30)
        max_temperature_label.setFixedWidth(30)
        temperature_slider_layout.setStretchFactor(min_temperature_label, 0)
        temperature_slider_layout.setStretchFactor(self.temperature_slider, 1)
        temperature_slider_layout.setStretchFactor(max_temperature_label, 0)
        self.window.assign_css_class(min_temperature_label, "slider_value_label")
        self.window.assign_css_class(max_temperature_label, "slider_value_label")
        # Adjust slider's settings
        self.temperature_slider.setMinimum(0)
        self.temperature_slider.setMaximum(20)
        self.temperature_slider.setTickInterval(1)
        self.temperature_slider.setSingleStep(1)
        self.temperature_slider.valueChanged.connect(self.on_temperature_slider_changed)
        # Add widgets and slider's layout to modal's layout
        self.modal_layout.addWidget(select_temperature_label)
        temperature_slider_layout.addWidget(min_temperature_label)
        temperature_slider_layout.addWidget(self.temperature_slider)
        temperature_slider_layout.addWidget(max_temperature_label)
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
        select_tokens_label = QLabel("Massimo numero di Token")
        tokens_slider_layout = QHBoxLayout()
        min_tokens_label = QLabel("1000")
        self.max_tokens_label = QLabel("10000")
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
        self.tokens_slider.setMinimum(1000)
        self.tokens_slider.setMaximum(10000)
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

    def add_line_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setMaximumHeight(1)
        self.window.assign_css_class(line, "line_separator")
        layout.addWidget(line)

    def on_confirm_button(self):
        """ Creates button to confirm llm selection """
        confirm_button = QPushButton("Conferma")
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
