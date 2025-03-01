from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class CurrentSettings(QObject):

    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.current_llm = None
        self.llms = [
            "GPT-4o mini",
            "GPT-4o",
            "GPT-4",
            "GPT-4 Turbo",
            "GPT-4.5 preview",
            "Gemini 2.0 Flash",
            "Gemini 1.5 Flash",
            "Gemini 1.5 Pro",
            "DeepSeek-V3",
            "DeepSeek-R1",
            "Mistral Small",
            "Pixtral",
            "Command",
            "Command R",
            "Command R+",
            "Llama70B",
            "Qwen2.5-32B",
            "Claude 3 Haiku",
            "Claude 3 Opus",
            "Claude 3 Sonnet",
            "Claude 3.5 Sonnet",
            "DALL-E 2",
            "DALL-E 3",
        ]
        self.widget_container = QWidget(objectName="current_settings_widget")
        self.on_current_settings_layout()

    def on_current_settings_layout(self):
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

        common = (
            f"<b>ID</b>: {self.chat_id}<br>"
            f"<b>Name</b>: {self.chat_custom_name or 'Name not set'}<br>"
            f"<b>Model</b>: {self.current_llm}<br>"
        )

        if self.current_llm not in ["DALL-E 2", "DALL-E 3"]:
            extra = (
                f"<b>Temperature</b>: {self.current_temperature}<br>"
                f"<b>Max tokens</b>: {self.current_max_tokens}<br>"
            )
        else:
            extra = (
                f"<b>Size</b>: {self.current_image_size}<br>"
                f"<b>Quality</b>: {self.current_image_quality}<br>"
                f"<b>N. of images</b>: {self.current_image_quantity}<br>"
            )

        last_message = f"<b>Last message</b>: {self.current_chat_date or 'Just created'}"
        settings_string = f"<div>{common}{extra}{last_message}</div>"
        self.current_settings_label.setText(settings_string)

    def on_show_sidebar_settings_label(self):
        """ Shows settings label on call """
        self.widget_container.show()

    def on_hide_sidebar_settings_label(self):
        """ Hides settings label on call """
        self.widget_container.hide()
