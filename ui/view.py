from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QSplashScreen
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Slot

from .status_bar import StatusBar
from .tool_bar import ToolBar
from .chat_log import ChatLog
from .sidebar.parent_sidebar import Sidebar
from .modals.add_api_key_modal import AddAPIKeyModal
from .modals.manage_api_keys_modal import ManageAPIKeysModal
from .modals.warning_modal import WarningModal


class LoadingScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setPixmap(QPixmap("ui/assets/img/loading_screen.png"))


class View(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gila")
        self.resize(1024, 768)
        self.setStyleSheet(self.load_css_file())
        self.create_layout()

    def create_layout(self):
        """ Creates layout for the window and composes UI """
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.status_bar = StatusBar(self)
        self.toolbar = ToolBar(self)
        self.sidebar = Sidebar(self)
        self.chat = ChatLog(self)
        self.add_api_key_modal = AddAPIKeyModal(self)
        self.manage_api_keys_modal = ManageAPIKeysModal(self)
        self.warning_modal = WarningModal(self)
        self.addToolBar(self.toolbar)
        self.setStatusBar(self.status_bar)
        main_layout = QGridLayout(central_widget)
        main_layout.addWidget(self.sidebar.widget_container, 0, 0)
        main_layout.addWidget(self.chat.widget_container, 0, 1, 1, 3)
        self.on_hide_chatlog_and_prompt_line()

    def load_css_file(self):
        """ Loads CSS File to apply style window """
        with open("ui/assets/styles.css", "r") as file:
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
