import os
import pickle

import markdown
import tiktoken

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                               QPushButton, QLabel, QSizePolicy, QApplication)


class Tokenizer:

    def __init__(self):
        pass

    def get_num_of_tokens(self, text):
        encoding = tiktoken.get_encoding("cl100k_base")
        encoding.encode(text)
        num_tokens = len(encoding.encode(text))
        return num_tokens


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
        self.tokenizer = Tokenizer()

        self.on_chat_container()

    def on_chat_container(self):
        """ Creates Chat layout and calls methods that adds widgets """
        chat_layout = QVBoxLayout(self.widget_container)
        self.title = QLabel("GILA", objectName="chat_title_label")
        self.title.setAlignment(Qt.AlignCenter)
        chat_layout.addWidget(self.title)
        chat_layout.addLayout(self.on_chatlog_info_layout())
        chat_layout.addWidget(self.log_widget, stretch=7)
        chat_layout.addLayout(self.prompt_layout.on_prompt_layout(), stretch=3)
        chat_layout.addLayout(self.on_prompt_info_layout())
        chat_layout.addLayout(self.on_start_layout())

    def update_chat_title(self):
        self.title.setText(f"{self.window.sidebar.current_settings.current_llm}")

    def on_prompt_info_layout(self):
        self.prompt_info_layout = QHBoxLayout()
        self.num_of_words = QLabel("Words: 0")
        self.num_of_tokens = QLabel("Tokens: 0")
        self.window.assign_css_class(self.num_of_words, "chatlog_info_labels")
        self.window.assign_css_class(self.num_of_tokens, "chatlog_info_labels")
        self.prompt_info_layout.addWidget(self.num_of_words)
        self.prompt_info_layout.addWidget(self.num_of_tokens)
        return self.prompt_info_layout

    def on_chatlog_info_layout(self):
        self.chatlog_info_layout = QHBoxLayout()
        self.first_label = QLabel("")
        self.second_label = QLabel("")
        self.third_label = QLabel("")
        self.chatlog_info_labels = [self.first_label, self.second_label, self.third_label]
        for label in self.chatlog_info_labels:
            self.window.assign_css_class(label, "chatlog_info_labels")
        self.chatlog_info_layout.addWidget(self.first_label)
        self.chatlog_info_layout.addWidget(self.second_label)
        self.chatlog_info_layout.addWidget(self.third_label)
        return self.chatlog_info_layout

    def words_counter(self):
        text = self.prompt_layout.prompt_box.toPlainText()
        word_count = len(text.split())
        self.num_of_words.setText(f"Words: {word_count}")

    def tokens_counter(self):
        num_tokens = self.tokenizer.get_num_of_tokens(self.prompt_layout.prompt_box.toPlainText())
        self.num_of_tokens.setText(f"Tokens: {num_tokens}")

    def on_start_layout(self):
        """ Creates Start layout with a button to start new chat """
        start_layout = QVBoxLayout()
        self.gila_image = QLabel(objectName="start_image")
        self.gila_image.setPixmap(QPixmap("storage/assets/icons/gila_logo.svg"))
        self.start_chat_button = QPushButton("New Chat")
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
            # Shows a cursor spinning wheel when waiting for response
            QApplication.setOverrideCursor(Qt.WaitCursor)
            # Append user prompt to log view window
            self.log_widget.append(
                f"<p><b>Tu</b>: {prompt}</p>")
        else:
            self.update_status_bar_from_chatlog.emit(
                "It is not possible to send an empty message.")

    def add_log_to_saved_chat_data(self, chat_id):
        with open(f'storage/saved_data/{chat_id}.pk', 'rb') as file:
            saved_data = pickle.load(file)
        saved_data[chat_id]["chat_log"] = self.get_chat_log()
        with open(f'storage/saved_data/{chat_id}.pk', 'wb') as file:
            pickle.dump(saved_data, file)

    def on_show_chatlog(self):
        """ Shows chat widget and start chat button on call """
        self.title.show()
        self.log_widget.show()
        for label in self.chatlog_info_labels:
            label.show()
        self.num_of_words.show()
        self.num_of_tokens.show()
        self.gila_image.hide()
        self.start_chat_button.hide()

    def on_hide_chatlog(self):
        """ Hides chat widget and start chat button on call """
        self.title.hide()
        self.log_widget.hide()
        for label in self.chatlog_info_labels:
            label.hide()
        self.num_of_words.hide()
        self.num_of_tokens.hide()
        self.gila_image.show()
        self.start_chat_button.show()

    @Slot(str)
    def get_response_message_slot(self, response):
        """ Slot
        Connected to one signal:
            - controller.response_message_to_chatlog
        Adds API response to Chat Log
        """
        self.prompt_layout.send_button.setEnabled(True)
        QApplication.restoreOverrideCursor()
        self.log_widget.append(f"<b>Gila</b>: {response}")

    @Slot(dict)
    def get_response_info_slot(self, response_info):
        for i, (key, value) in enumerate(response_info.items()):
            self.chatlog_info_labels[i].setText(f"{key}: {value}")

    def on_response_info_labels_reset(self):
        for label in self.chatlog_info_labels:
            label.setText("")

    def chatlog_has_text(self):
        """ Returns True if log_widget has text, else False """
        return bool(self.log_widget.toPlainText())

    def chatlog_has_changed(self, chat_id):
        file_path = f'storage/saved_data/{chat_id}.pk'
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                saved_data = pickle.load(file)
            chat_log = saved_data[chat_id]["chat_log"]
            if self.log_widget.toPlainText() == chat_log:
                return False
            return True
        return True

    def get_chat_log(self):
        """ Returns all current chat text """
        return self.log_widget.toHtml()

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
        self.prompt_box = CustomTextEdit(objectName="prompt_box_widget")
        self.prompt_box.textChanged.connect(self.chatlog.words_counter)
        self.prompt_box.textChanged.connect(self.chatlog.tokens_counter)

    def on_prompt_layout(self):
        """ Creates prompt layout with prompt box and a button """
        prompt_layout = QHBoxLayout(objectName="prompt_layout")
        # Adds prompt box
        self.prompt_box.returnPressed.connect(
            lambda: self.handle_user_prompt("none"))
        self.prompt_box.setFocus()
        prompt_layout.addWidget(self.prompt_box)
        # Adds send button
        self.send_button = QPushButton("Submit", objectName="enter_button")
        self.send_button.setFixedWidth(50)
        self.send_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.send_button.clicked.connect(
            lambda: self.handle_user_prompt("none"))
        prompt_layout.addWidget(self.send_button)
        return prompt_layout

    def handle_user_prompt(self, user_prompt):
        """ Gets user prompt from prompt box and calls process_prompt method from chatlog """
        prompt = self.prompt_box.toPlainText().strip() if user_prompt == "none" else user_prompt
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
