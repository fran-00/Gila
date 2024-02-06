from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout

from .status_bar import StatusBar
from .tool_bar import ToolBar
from .chat_log import ChatLog
from .sidebar import Sidebar


class View(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Metis")
        self.resize(1024, 768)
        self.setStyleSheet(self.load_css_file())
        self.create_layout()

    def create_layout(self):
        """Create a vertical layout for the window"""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.status_bar = StatusBar(self)
        self.toolbar = ToolBar(self)
        self.sidebar = Sidebar(self)
        self.chat = ChatLog(self)
        self.modal = MissingAPIKeyModal(self)

        self.addToolBar(self.toolbar.on_toolbar())
        self.setStatusBar(self.status_bar.status_bar)
        main_layout = QGridLayout(central_widget)
        main_layout.addLayout(self.sidebar.on_sidebar_layout(), 0, 0)
        main_layout.addLayout(self.chat.on_chat_layout(), 0, 1, 1, 3)
        self.on_hide_chatlog_and_prompt_line()

    def load_css_file(self):
        with open("ui/styles.css", "r") as file:
            return file.read()

    def on_hide_chatlog_and_prompt_line(self):
        self.chat.on_hide_chatlog()
        self.chat.prompt_layout.on_hide_prompt_layout()

    def on_show_chatlog_and_prompt_line(self):
        self.chat.on_show_chatlog()
        self.chat.prompt_layout.on_show_prompt_layout()
