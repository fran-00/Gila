from PySide6.QtWidgets import QHBoxLayout, QPushButton, QLineEdit


class UserPrompt:
    def __init__(self, view):
        self.view = view

    def on_prompt_layout(self):
        """Add horizzontal input box and a send button to submit"""
        self.view.prompt_box = QLineEdit()
        self.view.prompt_box.returnPressed.connect(
            lambda: self.view.handle_user_prompt("none"))

        # Button to submit input
        send_button = QPushButton("Enter", objectName="enter_button")
        send_button.clicked.connect(
            lambda: self.view.handle_user_prompt("none"))

        # Horizontal layout for input box and button
        prompt_layout = QHBoxLayout(objectName="prompt_layout")
        prompt_layout.addWidget(self.view.prompt_box)
        prompt_layout.addWidget(send_button)

        return prompt_layout
