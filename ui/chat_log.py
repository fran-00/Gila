from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton


class ChatLog:
    def __init__(self, window):
        self.window = window
        self.chat_view = ChatWidget(self.window).on_chat_widget()
        self.prompt_layout = PromptLayout(self.window).on_prompt_layout()

    def on_chat_layout(self):
        chat_layout = QVBoxLayout(objectName="chat_layout")
        chat_layout.addWidget(self.chat_view)
        chat_layout.addLayout(self.prompt_layout)
        return chat_layout

class ChatWidget:
    def __init__(self, window):
        self.chat_widget = QTextEdit()

    def on_chat_widget(self):
        self.chat_widget.setReadOnly(True)
        self.chat_widget.ensureCursorVisible()
        return self.chat_widget

    def get_chat_log(self):
        return self.chat_widget.toPlainText()


class PromptLayout:
    def __init__(self, window):
        self.window = window
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
        return self.window.process_prompt(prompt)

    def clear_prompt_box(self):
        self.prompt_box.clear()
        self.prompt_box.setFocus()
