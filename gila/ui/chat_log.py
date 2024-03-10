import pickle

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QPixmap, Qt


class Chat(QObject):
    user_prompt_signal_to_controller = Signal(str)
    update_status_bar_from_chatlog = Signal(str)
    start_new_chat_to_controller = Signal()

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.widget_container = QWidget(objectName="chat_container")

        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.ensureCursorVisible()
        self.prompt_layout = Prompt(self)

        self.on_chat_container()

    def on_chat_container(self):
        """ Creates Chat layout and calls methods that adds widgets """
        chat_layout = QVBoxLayout(self.widget_container)
        chat_layout.addWidget(self.log_widget)
        chat_layout.addLayout(self.on_start_layout())
        chat_layout.addLayout(self.prompt_layout.on_prompt_layout())

    def on_start_layout(self):
        """ Creates Start layout with a button to start new chat """
        start_layout = QVBoxLayout()
        self.gila_image = QLabel(objectName="start_image")
        self.gila_image.setPixmap(QPixmap("storage/assets/icons/gila_logo.svg"))
        self.start_chat_button = QPushButton("Nuova Conversazione")
        self.start_chat_button.clicked.connect(
            lambda: self.on_starting_a_new_chat())
        start_layout.addWidget(self.gila_image, alignment=Qt.AlignmentFlag.AlignCenter)
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
            self.log_widget.append(
                f"<p><b>Tu</b>: {prompt}</p>")
        else:
            self.update_status_bar_from_chatlog.emit(
                f"Non è possibile inviare un messaggio vuoto.")

    def add_log_to_saved_chat_data(self, chat_id):
        with open(f'storage/saved_data/{chat_id}.pk', 'rb') as file:
            saved_data = pickle.load(file)
        saved_data[chat_id]["chat_log"] = self.get_chat_log()
        with open(f'storage/saved_data/{chat_id}.pk', 'wb') as file:
            pickle.dump(saved_data, file)

    def on_show_chatlog(self):
        """ Shows chat widget and start chat button on call """
        self.log_widget.show()
        self.gila_image.hide()
        self.start_chat_button.hide()

    def on_hide_chatlog(self):
        """ Hides chat widget and start chat button on call """
        self.log_widget.hide()
        self.gila_image.show()
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
        self.log_widget.append(f"<b>Assistente</b>: {response}")

    def chatlog_has_text(self):
        """ Returns True if log_widget has text, else False """
        return bool(self.log_widget.toPlainText())

    def get_chat_log(self):
        """ Returns all current chat text """
        return self.log_widget.toPlainText()

    def on_starting_a_new_chat(self):
        """ Sends a signal to start a new chat """
        self.start_new_chat_to_controller.emit()


class CustomTextEdit(QTextEdit):
    returnPressed = Signal()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.returnPressed.emit()
        else:
            super().keyPressEvent(event)


class Prompt:
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
