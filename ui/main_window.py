from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from .chat_log import ChatLog
from .sidebar import Sidebar


class MainWindow(QMainWindow):

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
        self.sidebar = Sidebar(self)
        self.chat = ChatLog(self)

        main_layout = QHBoxLayout(central_widget)
        main_layout.addLayout(self.sidebar.on_sidebar_layout())
        main_layout.addLayout(self.chat.on_chat_layout())

    def load_css_file(self):
        with open("ui/styles.css", "r") as file:
            return file.read()
