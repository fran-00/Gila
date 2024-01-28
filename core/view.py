from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtCore import Signal, Slot

from ui.chat_log import ChatLog
from ui.sidebar import Sidebar


class View(QMainWindow):
    view_signal_to_controller = Signal(str)

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

    def process_prompt(self, prompt):
        # Emits the signal that contains user prompt
        self.view_signal_to_controller.emit(prompt)
        # Append user prompt to log view window
        self.chat.chat_view.append(
            f"<p><b>Tu</b>: {prompt}</p>")

    @Slot(str)
    def handle_ai_response(self, response):
        """ Slot that receives a string from controller as a signal """
        # Append output to chat view window
        self.chat.chat_view.append(f"<b>Assistente</b>: {response}")
