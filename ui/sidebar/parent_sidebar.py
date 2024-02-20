from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox
from PySide6.QtCore import QObject, Signal

from .stored_chats import StoredChats
from .current_settings import CurrentSettings


class Sidebar(QObject):
    selected_client_to_controller = Signal(str)

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.widget = QWidget(objectName="sidebar_container")
        self.stored_chats = StoredChats(self)
        self.current_settings = CurrentSettings(self)
        self.on_sidebar_container()

    def on_sidebar_container(self):
        """ Creates Sidebar layout and calls methods that adds widgets """
        sidebar_layout = QVBoxLayout(self.widget)
        sidebar_layout.addWidget(self.stored_chats.widget)
        sidebar_layout.addWidget(self.current_settings.widget)
        sidebar_layout.addWidget(self.on_llms_combobox())
        sidebar_layout.addWidget(self.on_confirm_button())
        self.current_settings.on_hide_widgets()

    def on_llms_combobox(self):
        """ Creates ComboBox with llms list """
        self.llms_combobox = QComboBox()
        for llm in self.current_settings.llms:
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
