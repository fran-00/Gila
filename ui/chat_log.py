from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton
from PySide6.QtCore import QObject, Signal, Slot


class Chat(QObject):
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

    def on_chat_container(self):
        """ Creates Chat layout and calls methods that adds widgets """
        chat_container = QWidget(objectName="chat_container")
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.addWidget(self.chat_widget)
        chat_layout.addLayout(self.on_start_layout())
        chat_layout.addLayout(self.prompt_layout.on_prompt_layout())
        return chat_container

    def on_start_layout(self):
        """ Creates Start layout with a button to start new chat """
        start_layout = QVBoxLayout(objectName="start_layout")
        self.start_chat_button = QPushButton("Nuova Conversazione")
        self.start_chat_button.clicked.connect(
            lambda: self.on_starting_a_new_chat())
        start_layout.addWidget(self.start_chat_button)
        start_layout.setStretch(0, 1)
        start_layout.setStretch(1, 1)
        return start_layout

    def process_prompt(self, prompt):
        """ Process user prompt, appends it to chatlog and sends it as a Signal
            to controller
        """
        if prompt != "":
            self.prompt_layout.send_button.setEnabled(False)
            self.user_prompt_signal_to_controller.emit(prompt)
            # Append user prompt to log view window
            self.chat_widget.append(
                f"<p><b>Tu</b>: {prompt}</p>")
        else:
            self.update_status_bar_from_chatlog.emit(
                f"Non è possibile inviare un messaggio vuoto.")

    def on_show_chatlog(self):
        """ Shows chat widget and start chat button on call """
        self.chat_widget.show()
        self.start_chat_button.hide()

    def on_hide_chatlog(self):
        """ Hides chat widget and start chat button on call """
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
        """ Returns all current chat text """
        return self.chat_widget.toPlainText()

    def on_starting_a_new_chat(self):
        """ Sends a signal to start a new chat """
        self.start_new_chat_to_controller.emit()


class PromptLayout:
    def __init__(self, chatlog):
        self.chatlog = chatlog
        self.prompt_box = QLineEdit()

    def on_prompt_layout(self):
        """ Creates prompt layout with prompt box and a button """
        prompt_layout = QHBoxLayout(objectName="prompt_layout")
        # Adds prompt box
        self.prompt_box.returnPressed.connect(
            lambda: self.handle_user_prompt("none"))
        self.prompt_box.setFocus()
        prompt_layout.addWidget(self.prompt_box)
        # Adds send button
        self.send_button = QPushButton("Enter", objectName="enter_button")
        self.send_button.clicked.connect(
            lambda: self.handle_user_prompt("none"))
        prompt_layout.addWidget(self.send_button)
        return prompt_layout

    def handle_user_prompt(self, user_prompt):
        """ Gets user prompt from prompt box and calls process_prompt method from chatlog """
        prompt = self.prompt_box.text().strip() if user_prompt == "none" else user_prompt
        self.clear_prompt_box()
        return self.chatlog.process_prompt(prompt)

    def clear_prompt_box(self):
        """ Clear prompt layout on call """
        self.prompt_box.clear()
        self.prompt_box.setFocus()

    def on_show_prompt_layout(self):
        """ Shows prompt layout and send button on call """
        self.prompt_box.show()
        self.send_button.show()

    def on_hide_prompt_layout(self):
        """ Hides prompt layout and send button on call """
        self.prompt_box.hide()
        self.send_button.hide()
