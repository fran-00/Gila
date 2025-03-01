import os
import pickle

import markdown
import tiktoken

from PySide6.QtCore import QObject, QSize, Signal, Slot, QTimer
from PySide6.QtGui import QAction, QIcon, QPixmap, Qt
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


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

        self.log_widget = CustomWebView()
        self.chat_html_logs = []
        self.prompt_layout = Prompt(self)
        self.tokenizer = Tokenizer()

        self.on_chat_container()

    def generate_chat_html(self):
        """ Updates chat log by generating an HTML page that includes chat 
            history and applies custom styling from a CSS file
        """
        chat_content = "".join(self.chat_html_logs)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        css_path = os.path.join(BASE_DIR, "storage", "assets", "chatlog-styles.css")
        css_content = ""
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()
        html_template = f"""
            <html>
                <head>
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/default.min.css">
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
                    <script>hljs.highlightAll();</script>
                </head>
                <style>
                    {css_content}
                </style>
                <body>
                    {chat_content}
                    <script>
                        function scrollToLatestMessage() {{
                            let messages = document.getElementsByClassName('user-wrapper');
                            if (messages.length > 0) {{
                                let lastMessage = messages[messages.length - 1];
                                lastMessage.scrollIntoView({{ behavior: 'smooth' }});
                            }}
                        }}
                        scrollToLatestMessage();
                    </script>
                </body>
            </html>
        """
        self.log_widget.setHtml(html_template)

    def on_chat_container(self):
        """ Creates Chat layout and calls methods that adds widgets """
        chat_layout = QVBoxLayout(self.widget_container)
        self.title = QLabel("GILA", objectName="chat_title_label")
        self.title.setAlignment(Qt.AlignCenter)
        chat_layout.addWidget(self.title)
        chat_layout.addLayout(self.on_chatlog_info_layout())
        chat_layout.addWidget(self.log_widget, stretch=8)
        chat_layout.addLayout(self.prompt_layout.on_prompt_layout(), stretch=2)
        chat_layout.addLayout(self.on_prompt_info_layout())
        chat_layout.addLayout(self.on_start_layout(), stretch=1000)

    def on_start_layout(self):
        """ Creates Start layout with a button to start new chat """
        start_layout = QVBoxLayout()
        self.start_inner_widget = QWidget()
        start_inner_layout = QVBoxLayout(self.start_inner_widget)
        gila_title = QLabel("GILA", objectName="gila_title")
        gila_image = QLabel(objectName="start_image")
        gila_image.setPixmap(QPixmap("storage/assets/icons/gila_logo.svg"))
        start_chat_button = QPushButton("New Chat")
        start_chat_button.clicked.connect(
            lambda: self.on_starting_a_new_chat()
        )
        start_inner_layout.addWidget(gila_title, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)
        start_inner_layout.addWidget(gila_image, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1000)
        start_inner_layout.addWidget(start_chat_button, stretch=1)
        start_layout.addWidget(self.start_inner_widget, stretch=1000)
        return start_layout

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

    def process_prompt(self, prompt):
        """ Process user prompt, appends it to chatlog and sends it as a Signal
            to controller
        """
        if prompt != "":
            self.chat_html_logs.append(f"""
                <div class='user-wrapper'>
                    <p class='prompt'>{prompt}</p>
                </div>
            """)
            # Update html page with new user prompt
            self.generate_chat_html()
            # Disable button
            self.prompt_layout.send_button.setEnabled(False)
            # Shows a cursor spinning wheel when waiting for response
            QApplication.setOverrideCursor(Qt.WaitCursor)
            # Shows a message in the status bar
            self.update_status_bar_from_chatlog.emit("I'm sending the message...")
            # Send the signal with user prompt with a delay of 0.1 seconds
            self.timer = QTimer()
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(lambda: self._send_delayed_prompt_signal(prompt))
            self.timer.start(100)
        else:
            self.update_status_bar_from_chatlog.emit(
                "It is not possible to send an empty message.")

    def _send_delayed_prompt_signal(self, prompt):
        self.user_prompt_signal_to_controller.emit(prompt)

    def add_log_to_saved_chat_data(self, chat_id):
        with open(f'storage/saved_data/{chat_id}.pk', 'rb') as file:
            saved_data = pickle.load(file)
        saved_data[chat_id]["chat_log"] = self.get_chat_log()
        with open(f'storage/saved_data/{chat_id}.pk', 'wb') as file:
            pickle.dump(saved_data, file)

    def on_show_chatlog(self):
        """ Shows chat widget and start chat button on call """
        self.title.show()
        self.generate_chat_html()
        self.log_widget.show()
        for label in self.chatlog_info_labels:
            label.show()
        self.num_of_words.show()
        self.num_of_tokens.show()
        self.start_inner_widget.hide()

    def on_hide_chatlog(self):
        """ Hides chat widget and start chat button on call """
        self.title.hide()
        self.log_widget.hide()
        for label in self.chatlog_info_labels:
            label.hide()
        self.num_of_words.hide()
        self.num_of_tokens.hide()
        self.start_inner_widget.show()

    def convert_markdown_to_html(self, md_text):
        """Converts Markdown to HTML"""
        return markdown.markdown(
            md_text, extensions=["fenced_code", "codehilite", "tables"]
        )

    @Slot(str)
    def get_response_message_slot(self, response):
        """ Slot
        Connected to one signal:
            - controller.response_message_to_chatlog
        Adds API response to Chat Log
        """
        self.prompt_layout.send_button.setEnabled(True)
        QApplication.restoreOverrideCursor()

        formatted_response = self.convert_markdown_to_html(response)
        if self.window.sidebar.current_settings.current_llm in ["DALL-E 2", "DALL-E 3"]:
            formatted_response = f"<div class='img-wrapper'><img src='{response}' class='img'></div>"
        self.chat_html_logs.append(f"""
            <div class='ai-wrapper'>
                <p class='response'>{formatted_response}</p>
            </div>
        """)
        self.generate_chat_html()

    @Slot(dict)
    def get_response_info_slot(self, response_info):
        for i, (key, value) in enumerate(response_info.items()):
            self.chatlog_info_labels[i].setText(f"{key}: {value}")

    def on_response_info_labels_reset(self):
        for label in self.chatlog_info_labels:
            label.setText("")

    def chatlog_has_text(self):
        """ Returns True if log_widget has text, else False """
        return bool(self.chat_html_logs)

    def chatlog_has_changed(self, chat_id):
        file_path = f'storage/saved_data/{chat_id}.pk'
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                saved_data = pickle.load(file)
            saved_chat_html_logs = saved_data[chat_id]["chat_log"]
            return self.chat_html_logs != saved_chat_html_logs
        return True

    def get_chat_log(self):
        """ Returns all current chat text """
        return self.chat_html_logs

    def on_starting_a_new_chat(self):
        """ Sends a signal to start a new chat """
        self.start_new_chat_to_controller.emit()


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
        self.send_button = QPushButton(objectName="enter_button")
        pixmap = QPixmap("storage/assets/icons/send-message.png")
        pixmap = pixmap.scaled(QSize(30, 30))
        send_icon = QIcon(pixmap)
        self.send_button.setIcon(send_icon)
        self.send_button.setIconSize(QSize(30, 30))
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


class CustomTextEdit(QTextEdit):
    returnPressed = Signal()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.returnPressed.emit()
        else:
            super().keyPressEvent(event)


class CustomWebView(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_custom_menu)

    def show_custom_menu(self, pos):
        menu = QMenu(self)

        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_selected_text)

        menu.addAction(copy_action)
        menu.exec(self.mapToGlobal(pos))

    def copy_selected_text(self):
        self.page().triggerAction(QWebEnginePage.Copy)
