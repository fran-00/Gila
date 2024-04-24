from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (QMainWindow, QWidget, QGridLayout, 
                               QSplashScreen, QPushButton, QSizePolicy)

from .status_bar import StatusBar
from .tool_bar import ToolBar
from .chat_log import Chat
from .sidebar.parent_sidebar import Sidebar
from .modals.add_api_key_modal import AddAPIKeyModal
from .modals.manage_api_keys_modal import ManageAPIKeysModal
from .modals.warning_modal import WarningModal
from .modals.about_gila_modal import AboutGilaModal


class LoadingScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setPixmap(QPixmap("storage/assets/img/loading_screen.png"))


class View(QMainWindow):
    window_closed_signal_to_controller = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gila")
        self.setWindowIcon(QIcon("storage/assets/icons/gila_logo.svg"))
        self.resize(800, 600)
        self.setStyleSheet(self.load_css_file())
        self.create_layout()

    def create_layout(self):
        """ Creates layout for the window and composes UI """
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.status_bar = StatusBar(self)
        self.toolbar = ToolBar(self)
        self.sidebar = Sidebar(self)
        self.chat = Chat(self)
        self.add_api_key_modal = AddAPIKeyModal(self)
        self.manage_api_keys_modal = ManageAPIKeysModal(self)
        self.warning_modal = WarningModal(self)
        self.about_gila_modal = AboutGilaModal(self)
        self.addToolBar(self.toolbar)
        self.setStatusBar(self.status_bar)
        main_layout = QGridLayout(central_widget)
        main_layout.addWidget(self.sidebar.widget_container, 0, 0)
        main_layout.addWidget(self.on_toggle_sidebar_button(), 0, 1)
        main_layout.addWidget(self.chat.widget_container, 0, 2, 1, 3)
        self.on_hide_chatlog_and_prompt_line()

    def on_toggle_sidebar_button(self):
        self.toggle_sidebar_button = QPushButton("<", objectName="toggle_sidebar_button")
        self.toggle_sidebar_button.setFixedWidth(10)
        self.toggle_sidebar_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toggle_sidebar_button.clicked.connect(self.toggle_sidebar)
        return self.toggle_sidebar_button

    def toggle_sidebar(self):
        self.sidebar.widget_container.setVisible(not self.sidebar.widget_container.isVisible())
        if self.sidebar.widget_container.isVisible():
            self.toggle_sidebar_button.setText("<")
        else:
            self.toggle_sidebar_button.setText(">")

    def load_css_file(self):
        """ Loads CSS File to apply style window """
        with open("storage/assets/styles.css", "r") as file:
            return file.read()

    def on_hide_chatlog_and_prompt_line(self):
        """ Hides chat log and prompt box on call """
        self.chat.on_hide_chatlog()
        self.chat.prompt_layout.on_hide_prompt_layout()

    def on_show_chatlog_and_prompt_line(self):
        """ Show chat log and prompt box on call """
        self.chat.on_show_chatlog()
        self.chat.prompt_layout.on_show_prompt_layout()

    @Slot(str)
    def add_api_key_modal_slot(self, client_name):
        """ Slot
        Connected to one signal:
            - controller.missing_api_key_to_view
        Called also by view.manage_api_keys_modal passing client name as argument
        Shows AddAPIKeyModal when triggered
        """
        self.add_api_key_modal.client_name = client_name
        self.add_api_key_modal.update_modal_labels()
        self.add_api_key_modal.exec_()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.window_closed_signal_to_controller.emit()

    def assign_css_class(self, widget, class_name):
        widget.setProperty("class", class_name)
