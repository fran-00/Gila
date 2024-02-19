from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal


class CurrentSettings(QWidget):
    stop_chat_to_controller = Signal()

    def __init__(self, parent_layout):
        super().__init__()
        self.parent_layout = parent_layout
        self.current_llm = None
        self.current_temperature = None
        self.llms = [
            "GPT-4",
            "GPT-4 Turbo",
            "GPT-3.5 Turbo",
            "Gemini Pro",
            "Cohere Chat"
        ]
        self.setObjectName("current_settings_widget")
        self.on_current_settings_layout()

    def on_current_settings_layout(self):
        current_settings_layout = QVBoxLayout(self)
        current_settings_layout.addWidget(self.on_settings_label())
        current_settings_layout.addWidget(self.on_new_chat_button())
        return current_settings_layout

    def on_settings_label(self):
        """ Creates a label with current client's settings """
        self.current_settings_label = QLabel(
            f"- {self.current_llm}\n- {self.current_temperature}")
        return self.current_settings_label

    def on_new_chat_button(self):
        """ Creates a button to start a new chat """
        self.new_chat_button = QPushButton("Nuova Chat")
        self.new_chat_button.clicked.connect(self.send_stop_chat_to_controller)
        return self.new_chat_button

    def update_settings_label(self, settings):
        """ Called from Controller when new chat is started, return current settings """
        self.current_llm = settings[0]
        self.current_temperature = settings[1]
        self.current_settings_label.setText(
            f"- {self.current_llm}\n- {self.current_temperature}")

    def on_show_widgets(self):
        """ Shows settings label and new chat button on call """
        self.current_settings_label.show()
        self.new_chat_button.show()

    def on_hide_widgets(self):
        """ Hides settings label and new chat button on call """
        self.current_settings_label.hide()
        self.new_chat_button.hide()

    def send_stop_chat_to_controller(self):
        """ Sends a signal to stop current chat, connected to New Chat button"""
        self.stop_chat_to_controller.emit()
