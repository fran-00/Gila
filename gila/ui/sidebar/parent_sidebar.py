from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import QObject

from .stored_chats import StoredChats
from .current_settings import CurrentSettings
from ..modals.change_settings_modal import ChangeSettingsModal


class Sidebar(QObject):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.widget_container = QWidget(objectName="sidebar_container")
        self.stored_chats = StoredChats(self.widget_container)
        self.current_settings = CurrentSettings(self.widget_container)
        self.change_settings_modal = ChangeSettingsModal(self.window, self.current_settings)
        self.on_sidebar_container()

    def on_sidebar_container(self):
        """ Creates Sidebar layout and calls methods that adds widgets """
        sidebar_layout = QVBoxLayout(self.widget_container)
        sidebar_layout.addWidget(self.stored_chats.scroll_area)
        sidebar_layout.addWidget(self.current_settings.widget_container)
        sidebar_layout.addWidget(self.on_change_settings_button())
        self.current_settings.on_hide_widgets()

    def on_change_settings_button(self):
        change_settings_button = QPushButton("Modifica impostazioni")
        change_settings_button.clicked.connect(self.open_change_settings_modal)
        return change_settings_button

    def open_change_settings_modal(self):
        self.change_settings_modal.exec_()
