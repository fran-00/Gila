from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton
from PySide6.QtCore import QObject, Signal, Slot


class ChatLog(QObject):
    user_prompt_signal_to_controller = Signal(str)

    def __init__(self, window):
        super().__init__()

        self.window = window
        self.chat_widget = QTextEdit()
        self.chat_widget.setReadOnly(True)
        self.chat_widget.ensureCursorVisible()
        self.prompt_layout = PromptLayout(self)

    def on_chat_layout(self):
        chat_layout = QVBoxLayout(objectName="chat_layout")
        chat_layout.addWidget(self.chat_widget)
        chat_layout.addLayout(self.prompt_layout.on_prompt_layout())
        return chat_layout

    def process_prompt(self, prompt):
        # Emits the signal that contains user prompt
        self.user_prompt_signal_to_controller.emit(prompt)
        # Append user prompt to log view window
        self.chat_widget.append(
            f"<p><b>Tu</b>: {prompt}</p>")

    @Slot(str)
    def handle_ai_response(self, response):
        """ Slot that receives a string from controller as a signal """
        # Append output to chat view window
        self.chat_widget.append(f"<b>Assistente</b>: {response}")

    def get_chat_log(self):
        return self.chat_widget.toPlainText()


class PromptLayout:
    def __init__(self, chatlog):
        self.chatlog = chatlog
        self.prompt_box = QLineEdit()

    def on_prompt_layout(self):
        self.prompt_box.returnPressed.connect(
            lambda: self.handle_user_prompt("none"))
        self.prompt_box.setFocus()

        # Horizontal layout for input box and button
        prompt_layout = QHBoxLayout(objectName="prompt_layout")
        prompt_layout.addWidget(self.prompt_box)

        send_button = QPushButton("Enter", objectName="enter_button")
        send_button.clicked.connect(
            lambda: self.handle_user_prompt("none"))

        prompt_layout.addWidget(send_button)
        return prompt_layout

    def handle_user_prompt(self, user_prompt):
        prompt = self.prompt_box.text().strip() if user_prompt == "none" else user_prompt
        self.clear_prompt_box()
        return self.chatlog.process_prompt(prompt)

    def clear_prompt_box(self):
        self.prompt_box.clear()
        self.prompt_box.setFocus()
