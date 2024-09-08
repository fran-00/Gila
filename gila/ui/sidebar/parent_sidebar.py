from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from .stored_chats import StoredChats
from .current_settings import CurrentSettings
from ..modals.change_settings_modal import ChangeSettingsModal


class Sidebar(QObject):
    stop_chat_to_controller = Signal()

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.widget_container = QWidget(objectName="sidebar_container")
        self.widget_container.setFixedWidth(300)
        self.stored_chats = StoredChats(self)
        self.current_settings = CurrentSettings(self.widget_container)
        self.change_settings_modal = ChangeSettingsModal(self.window, self.current_settings)
        self.on_sidebar_container()

    def on_sidebar_container(self):
        """ Creates Sidebar layout and calls methods that adds widgets """
        sidebar_layout = QVBoxLayout(self.widget_container)
        sidebar_layout.addWidget(self.stored_chats.scroll_area)
        sidebar_layout.addWidget(self.current_settings.widget_container)
        sidebar_layout.addWidget(self.on_new_chat_button())
        self.current_settings.on_hide_widgets()
        self.on_hide_widgets()

    def on_new_chat_button(self):
        """ Creates a button to start a new chat """
        self.new_chat_button = QPushButton("New Chat")
        self.new_chat_button.clicked.connect(self.send_stop_chat_to_controller)
        return self.new_chat_button

    def open_change_settings_modal(self):
        self.change_settings_modal.exec_()

    def send_stop_chat_to_controller(self):
        """ Sends a signal to stop current chat, connected to New Chat button"""
        self.stop_chat_to_controller.emit()

    def on_show_widgets(self):
        """ Shows new chat button on call """
        self.new_chat_button.show()

    def on_hide_widgets(self):
        """ Hides new chat button on call """
        self.new_chat_button.hide()
