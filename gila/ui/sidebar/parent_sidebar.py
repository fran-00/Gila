from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTabWidget

from .stored_chats import StoredChats
from .change_settings import ChangeSettings
from .current_settings import CurrentSettings


class Sidebar(QObject):
    stop_chat_to_controller = Signal()

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.widget_container = QWidget(objectName="sidebar_container")
        self.widget_container.setFixedWidth(300)

        self.stored_chats = StoredChats(self)
        self.current_settings = CurrentSettings(self.widget_container)
        self.change_settings = ChangeSettings(self, self.current_settings)

        self.on_sidebar_container()

    def on_sidebar_container(self):
        """Create sidebar layout using QTabWidget to manage tabs"""
        sidebar_layout = QVBoxLayout(self.widget_container)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.stored_chats.scroll_area, "Saved Chats")
        self.tab_widget.addTab(self.change_settings.scroll_area, "Settings")
        sidebar_layout.addWidget(self.tab_widget)

        sidebar_layout.addWidget(self.current_settings.widget_container)
        sidebar_layout.addWidget(self.on_new_chat_button())

        self.current_settings.on_hide_widgets()
        # Hide sidebar's new_chat button cause on startup there's the main start button insead
        self.on_hide_sidebar_new_chat_button()

    def on_new_chat_button(self):
        """Creates a button to start a new chat"""
        self.new_chat_button = QPushButton("New Chat")
        self.new_chat_button.clicked.connect(self.send_stop_chat_to_controller)
        return self.new_chat_button

    def send_stop_chat_to_controller(self):
        """Sends a signal to stop current chat, connected to New Chat button"""
        self.stop_chat_to_controller.emit()

    def on_show_sidebar_new_chat_button(self):
        """ Shows new chat button on call """
        self.new_chat_button.show()

    def on_hide_sidebar_new_chat_button(self):
        """ Hides new chat button on call """
        self.new_chat_button.hide()
