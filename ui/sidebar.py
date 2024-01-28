from PySide6.QtWidgets import QVBoxLayout, QPushButton, QComboBox

from ai.manager import LLMsManager


class Sidebar:

    def __init__(self, window):
        self.window = window
        self.sidebar_view = LLMChanger().on_sidebar_widget()

    def on_sidebar_layout(self):
        sidebar_layout = QVBoxLayout(objectName="sidebar_layout")
        sidebar_layout.addWidget(self.sidebar_view)
        return sidebar_layout


class LLMChanger:

    def __init__(self):
        self.clients_manager = LLMsManager()
        self.sidebar_widget = QComboBox()

    def on_sidebar_widget(self):
        llms_list = self.clients_manager.available_models()
        for llm in llms_list:
            self.sidebar_widget.addItem(llm)
        return self.sidebar_widget
