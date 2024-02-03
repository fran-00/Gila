from PySide6.QtWidgets import QVBoxLayout, QPushButton, QComboBox, QLabel
from PySide6.QtCore import QObject, Signal, Slot


class Sidebar(QObject):
    selected_client_to_controller = Signal(str)
    stop_chat_to_controller = Signal()

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.current_llm = None
        self.current_temperature = None
        self.llms = [
            "GPT-4",
            "GPT-4 Turbo",
            "GPT-3.5 Turbo",
            "Gemini Pro",
            "Cohere Chat"
        ]

    def on_sidebar_layout(self):
        sidebar_layout = QVBoxLayout(objectName="sidebar_layout")
        sidebar_layout.addWidget(self.on_settings_label())
        sidebar_layout.addWidget(self.on_llms_combobox())
        sidebar_layout.addWidget(self.on_confirm_button())
        sidebar_layout.addWidget(self.on_new_chat_button())
        return sidebar_layout

    def on_llms_combobox(self):
        self.llms_combobox = QComboBox()
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

    @Slot(tuple)
    def get_current_settings_slot(self, settings):
        """ Get current llm """
        self.current_llm = settings[0]

    def send_selected_client_to_controller(self, llm):
        """ Send a signal to controller """
        self.selected_client_to_controller.emit(llm)

    def on_new_chat_button(self):
        new_chat_button = QPushButton("Nuova Chat")
        new_chat_button.clicked.connect(self.send_stop_chat_to_controller)
        return new_chat_button

    def send_stop_chat_to_controller(self):
        self.stop_chat_to_controller.emit()

    def on_settings_label(self):
        self.current_settings_label = QLabel(f"- {self.current_llm}\n- {self.current_temperature}")
        return self.current_settings_label

    def update_settings_label(self, settings):
        """ Called from Controller when new chat is started, return current settings """
        self.current_llm = settings[0]
        self.current_temperature = settings[1]
        self.current_settings_label.setText(f"- {self.current_llm}\n- {self.current_temperature}")
