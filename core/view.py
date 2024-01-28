from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Signal, Slot

from ui.chat_log import ChatWidget, PromptLayout


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

        self.chat_view = ChatWidget(self).on_chat_widget()
        self.prompt_layout = PromptLayout(self).on_prompt_layout()

        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(self.chat_view)
        main_layout.addLayout(self.prompt_layout)

    def load_css_file(self):
        with open("ui/styles.css", "r") as file:
            return file.read()

    def process_prompt(self, prompt):
        # Emits the signal that contains user prompt
        self.view_signal_to_controller.emit(prompt)
        # Append user prompt to log view window
        self.chat_view.append(
            f"<p><b>Tu</b>: {prompt}</p>")

    @Slot(str)
    def handle_ai_response(self, response):
        """ Slot that receives a string from controller as a signal """
        # Append output to chat view window
        self.chat_view.append(f"<b>Assistente</b>: {response}")
