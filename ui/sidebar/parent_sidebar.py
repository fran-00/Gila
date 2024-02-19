from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel
from PySide6.QtCore import QObject, Signal

from .stored_chats import StoredChats


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

    def on_sidebar_container(self):
        """ Creates Sidebar layout and calls methods that adds widgets """
        sidebar_container = QWidget(objectName="sidebar_container")
        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.addWidget(StoredChats(self.window))
        sidebar_layout.addWidget(self.on_current_settings_container())
        sidebar_layout.addWidget(self.on_llms_combobox())
        sidebar_layout.addWidget(self.on_confirm_button())
        self.on_hide_widgets()
        return sidebar_container

    def on_current_settings_container(self):
        current_settings_container = QWidget(objectName="current_settings_container")
        current_settings_layout = QVBoxLayout(current_settings_container)
        current_settings_layout.addWidget(self.on_settings_label())
        current_settings_layout.addWidget(self.on_new_chat_button())
        return current_settings_container

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

    def on_llms_combobox(self):
        """ Creates ComboBox with llms list """
        self.llms_combobox = QComboBox()
        for llm in self.llms:
            self.llms_combobox.addItem(llm)
        self.llms_combobox.currentIndexChanged.connect(
            self.on_combobox_changed)
        return self.llms_combobox

    def on_combobox_changed(self):
        pass

    def on_confirm_button(self):
        """ Creates button to confirm llm selection """
        confirm_button = QPushButton("Conferma")
        confirm_button.clicked.connect(self.send_selected_client_to_controller)
        return confirm_button

    def send_selected_client_to_controller(self):
        """ Sends selected llm to controller: signal is triggered when Confirm
            Button is pressed
        """
        selected_llm = self.llms_combobox.currentText()
        self.selected_client_to_controller.emit(selected_llm)

    def send_stop_chat_to_controller(self):
        """ Sends a signal to stop current chat, connected to New Chat button"""
        self.stop_chat_to_controller.emit()

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
