from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton
from PySide6.QtCore import QObject, Signal, Slot


class ChatLog(QObject):
    user_prompt_signal_to_controller = Signal(str)
    update_status_bar_from_chatlog = Signal(str)
    start_new_chat_to_controller = Signal()

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
        chat_layout.addLayout(self.on_start_layout())
        chat_layout.addLayout(self.prompt_layout.on_prompt_layout())
        return chat_layout

    def on_start_layout(self):
        start_layout = QVBoxLayout(objectName="start_layout")
        self.start_chat_button = QPushButton("Nuova Conversazione")
        self.start_chat_button.clicked.connect(
            lambda: self.on_starting_a_new_chat())
        start_layout.addWidget(self.start_chat_button)
        start_layout.setStretch(0, 1)
        start_layout.setStretch(1, 1)
        return start_layout

    def process_prompt(self, prompt):
        if prompt != "":
            self.prompt_layout.send_button.setEnabled(False)
            self.user_prompt_signal_to_controller.emit(prompt)
            # Append user prompt to log view window
            self.chat_widget.append(
                f"<p><b>Tu</b>: {prompt}</p>")
        else:
            self.update_status_bar_from_chatlog.emit(f"Non è possibile inviare un messaggio vuoto.")

    def on_show_chatlog(self):
        self.chat_widget.show()
        self.start_chat_button.hide()

    def on_hide_chatlog(self):
        self.chat_widget.hide()
        self.start_chat_button.show()

    @Slot(str)
    def get_ai_response_slot(self, response):
        """ Slot
        Connected to one signal:
            - controller.ai_response_to_chatlog
        Adds API response to Chat Log
        """
        self.prompt_layout.send_button.setEnabled(True)
        """ Slot that receives a string from controller as a signal """
        # Append output to chat view window
        self.chat_widget.append(f"<b>Assistente</b>: {response}")

    def get_chat_log(self):
        return self.chat_widget.toPlainText()

    def on_starting_a_new_chat(self):
        self.start_new_chat_to_controller.emit()


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

        self.send_button = QPushButton("Enter", objectName="enter_button")
        self.send_button.clicked.connect(
            lambda: self.handle_user_prompt("none"))

        prompt_layout.addWidget(self.send_button)
        return prompt_layout

    def handle_user_prompt(self, user_prompt):
        prompt = self.prompt_box.text().strip() if user_prompt == "none" else user_prompt
        self.clear_prompt_box()
        return self.chatlog.process_prompt(prompt)

    def clear_prompt_box(self):
        self.prompt_box.clear()
        self.prompt_box.setFocus()

    def on_show_prompt_layout(self):
        self.prompt_box.show()
        self.send_button.show()

    def on_hide_prompt_layout(self):
        self.prompt_box.hide()
        self.send_button.hide()
