import re

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from ..utils import FileHandler as FH


class CurrentSettings(QObject):

    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.current_llm = None
        self.llms = self._get_models_from_json()
        self.widget_container = QWidget(objectName="current_settings_widget")
        self._build_current_settings_layout()

    def _get_models_from_json(self):
        return list(FH.load_file("storage/assets/json/models.json").keys())

    def _build_current_settings_layout(self):
        current_settings_layout = QVBoxLayout(self.widget_container)
        self.current_settings_label = QLabel("", objectName="settings_label")
        current_settings_layout.addWidget(self.current_settings_label)
        return current_settings_layout

    def update_settings_label(self, settings):
        """ Called from Controller when new chat is started, return current settings """
        self.chat_id = settings[0]
        self.chat_custom_name = settings[1]
        self.current_llm = settings[2]
        self.current_temperature = settings[3]
        self.current_max_tokens = settings[4]
        self.current_chat_date = settings[5]
        self.current_image_size = settings[7]
        self.current_image_quality = settings[8]
        self.current_image_quantity = settings[9]
        self.current_reasoning_effort = settings[10]

        self.current_settings_label.setText(self._build_settings_str())

    def _build_settings_str(self):
        """Generates the HTML representation of the current settings."""

        def is_o_series():
            return re.match(r"^o\d+(-\w+)?$", self.current_llm)

        def is_dalle_model():
            return re.match(r"^DALL-E \d+", self.current_llm)

        settings = {
            "ID": self.chat_id,
            "Name": self.chat_custom_name or "Name not set",
            "Model": self.current_llm,
        }

        if is_o_series():
            settings["Reasoning effort"] = self.current_reasoning_effort
            settings["Max Completion tokens"] = self.current_max_tokens
        elif is_dalle_model():
            num_images = 1 if self.current_llm == "DALL-E 3" else self.current_image_quantity
            settings["Size"] = self.current_image_size
            settings["N. of images"] = num_images
            if self.current_llm == "DALL-E 3":
                settings["Quality"] = self.current_image_quality
        else:
            settings["Temperature"] = self.current_temperature
            settings["Max tokens"] = self.current_max_tokens

        settings["Last message"] = self.current_chat_date or "Just created"

        settings_lines = [f"<b>{key}</b>: {value}" for key, value in settings.items()]
        return f"<div>{'<br>'.join(settings_lines)}</div>"

    def show_sidebar_settings_label(self):
        """ Shows settings label on call """
        self.widget_container.show()

    def hide_sidebar_settings_label(self):
        """ Hides settings label on call """
        self.widget_container.hide()
