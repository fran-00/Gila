from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit
from PySide6.QtCore import Signal, Slot

from ui.widgets import UserPrompt


class View(QMainWindow):
    view_signal_to_controller = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Metis")
        self.resize(1024, 768)
        self.create_layout()

    def create_layout(self):
        """Create a vertical layout for the window"""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        chat_view = self.on_chat_view()
        prompt_layout = UserPrompt(self).on_prompt_layout()

        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(chat_view)
        main_layout.addLayout(prompt_layout)

        # Set focus on user prompt box
        self.prompt_box.setFocus()

    def on_chat_view(self):
        """Add widget for displaying chat log"""
        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)
        self.chat_view.ensureCursorVisible()

        return self.chat_view

    def get_chat_log(self):
        return self.chat_view.toPlainText()

    def handle_user_prompt(self, user_prompt):
        prompt = self.prompt_box.text().strip() if user_prompt == "none" else user_prompt
        return self.process_prompt(prompt)

    def process_prompt(self, prompt):
        # Emits the signal that contains user prompt
        self.view_signal_to_controller.emit(prompt)
        # Append user prompt to log view window
        self.chat_view.append(
            f"<p style='color:#ffdc7d; font-weight:600'>>>> {prompt}</p>")
        # Resets the prompt box
        self.prompt_box.clear()
        self.prompt_box.setFocus()

    @Slot(str)
    def handle_ai_response(self, response):
        """ Slot that receives a string from controller as a signal """
        # Append output to chat view window
        self.chat_view.append(f"{response}")
