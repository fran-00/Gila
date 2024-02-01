from PySide6.QtWidgets import QVBoxLayout, QPushButton, QComboBox
from PySide6.QtCore import QObject, Signal, Slot


class Sidebar(QObject):
    selected_client_to_controller = Signal(tuple)

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.llms_combobox = QComboBox()
        self.llms = [
            "GPT-4",
            "GPT-4 Turbo",
            "GPT-3.5 Turbo",
            "Gemini Pro",
            "Cohere Chat"
        ]

    def on_sidebar_layout(self):
        sidebar_layout = QVBoxLayout(objectName="sidebar_layout")
        sidebar_layout.addWidget(self.on_llms_combobox())
        sidebar_layout.addWidget(self.on_confirm_button())
        return sidebar_layout

    def on_llms_combobox(self):
        for llm in self.llms:
            self.llms_combobox.addItem(llm)
        self.llms_combobox.currentIndexChanged.connect(self.on_combobox_changed)
        return self.llms_combobox

    def on_combobox_changed(self):
        pass

    def on_confirm_button(self):
        confirm_button = QPushButton("Conferma")
        confirm_button.clicked.connect(self.set_client)
        return confirm_button

    def set_client(self):
        """ Trigger signal sending when Confirm Button is pressed"""
        selected_llm = self.llms_combobox.currentText()
        print(selected_llm)
        return self.send_selected_client_to_controller(selected_llm)

    @Slot(str)
    def get_current_client_from_controller(self, llm):
        """ Get current llm """
        self.current_llm = llm

    def send_selected_client_to_controller(self, llm):
        """ Send a signal to controller """
        self.selected_client_to_controller.emit(llm)
