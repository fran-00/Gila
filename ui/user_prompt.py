from PySide6.QtWidgets import QHBoxLayout, QPushButton, QLineEdit


class UserPrompt:
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
        return self.window.process_prompt(prompt)

    def clear_prompt_box(self):
        self.prompt_box.clear()
        self.prompt_box.setFocus()
