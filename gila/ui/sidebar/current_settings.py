from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class CurrentSettings(QObject):

    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.current_llm = None
        self.current_temperature = None
        self.llms = [
            "GPT-4",
            "GPT-4 Turbo",
            "GPT-3.5 Turbo",
            # "Gemini Pro",
            "Cohere Chat"
        ]
        self.widget_container = QWidget(objectName="current_settings_widget")
        self.on_current_settings_layout()

    def on_current_settings_layout(self):
        current_settings_layout = QVBoxLayout(self.widget_container)
        current_settings_layout.addWidget(self.on_settings_label())
        return current_settings_layout

    def on_settings_label(self):
        """ Creates a label with current client's settings """
        self.current_settings_label = QLabel(
            f"- {self.current_llm}\n- {self.current_temperature}")
        return self.current_settings_label

    def update_settings_label(self, settings):
        """ Called from Controller when new chat is started, return current settings """
        self.chat_id = settings[0]
        self.current_llm = settings[1]
        self.current_temperature = settings[2]
        self.current_settings_label.setText(
            f"- {self.chat_id}\n- {self.current_llm}\n- {self.current_temperature}")

    def on_show_widgets(self):
        """ Shows settings label on call """
        self.widget_container.show()

    def on_hide_widgets(self):
        """ Hides settings label on call """
        self.widget_container.hide()
