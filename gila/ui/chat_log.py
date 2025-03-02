import os
import pickle
import html
import bleach

import markdown

from PySide6.QtCore import QObject, QSize, Signal, Slot, QTimer
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .utils import CustomTextEdit, CustomWebView, Tokenizer


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
        """Generate an HTML page to update the chat log, including chat history 
        and custom styling from a CSS file.

        The method constructs an HTML template that incorporates the chat logs 
        stored in `self.chat_html_logs`, applies styles from a CSS file located 
        in the assets directory, and includes scripts for syntax highlighting 
        and automatic scrolling to the latest message. The final HTML is set to
        the chat log widget for display.
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
        """Create the chat layout and adds various widgets to the chat interface."""
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
        """Create the start layout with a button to initiate a new chat."""
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
        """Update the chat title to reflect the currently selected LLM setting."""
        self.title.setText(f"{self.window.sidebar.current_settings.current_llm}")

    def on_prompt_info_layout(self):
        """Create a horizontal layout for displaying prompt information."""
        self.prompt_info_layout = QHBoxLayout()
        self.num_of_words = QLabel("Words: 0")
        self.num_of_tokens = QLabel("Tokens: 0")
        self.window.assign_css_class(self.num_of_words, "chatlog_info_labels")
        self.window.assign_css_class(self.num_of_tokens, "chatlog_info_labels")
        self.prompt_info_layout.addWidget(self.num_of_words)
        self.prompt_info_layout.addWidget(self.num_of_tokens)
        return self.prompt_info_layout

    def on_chatlog_info_layout(self):
        """Create a horizontal layout for displaying chat log information labels."""
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
        """Count the number of words in the prompt box and updates the display."""
        text = self.prompt_layout.prompt_box.toPlainText()
        word_count = len(text.split())
        self.num_of_words.setText(f"Words: {word_count}")

    def tokens_counter(self):
        """Count the number of tokens in the prompt box and updates the display."""
        num_tokens = self.tokenizer.get_num_of_tokens(self.prompt_layout.prompt_box.toPlainText())
        self.num_of_tokens.setText(f"Tokens: {num_tokens}")

    def process_prompt(self, prompt):
        """Process the user prompt, appends it to the chat log, and sends it
        as a signal to the controller.

        This method performs the following actions:
        - Checks if the prompt is not empty.
        - Sanitizes the prompt using html.escape and bleach library.
        - Appends the sanitized prompt to the chat log in HTML format.
        - Updates the HTML page to reflect the new user prompt.
        - Disables the send button to prevent multiple submissions.
        - Changes the cursor to a wait cursor while processing the prompt.
        - Displays a message in the status bar indicating that the message is being sent.
        - Sends the user prompt as a signal after a delay of 0.1 seconds using a timer.

        If the prompt is empty, a message is emitted to the status bar indicating that 
        an empty message cannot be sent.

        Args:
            prompt (str): The user input prompt to be processed.
        """
        if prompt != "":
            escaped_prompt = html.escape(prompt)
            sanitized_prompt = bleach.clean(escaped_prompt)
            sanitized_prompt = sanitized_prompt.replace(" ", "&nbsp;")
            sanitized_prompt = sanitized_prompt.replace("\n", "<br>")

            self.chat_html_logs.append(f"""
                <div class='user-wrapper'>
                    <p class='prompt'>{sanitized_prompt}</p>
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
        """Emit the user prompt signal to the controller.

        Private method called after a delay to send the processed user 
        prompt to the controller.

        Args:
            prompt (str): The user input prompt to be sent to the controller.
        """
        self.user_prompt_signal_to_controller.emit(prompt)

    def add_log_to_saved_chat_data(self, chat_id):
        """Add the current chat log to the saved chat data for a specific chat ID.

        Opens the saved chat data file corresponding to the provided `chat_id` 
        and loads its contents using the `pickle` module, updates the chat log
        entry in the loaded data with the current chat log and saves the updated
        data back to the same file.
        """
        with open(f'storage/saved_data/{chat_id}.pk', 'rb') as file:
            saved_data = pickle.load(file)
        saved_data[chat_id]["chat_log"] = self.get_chat_log()
        with open(f'storage/saved_data/{chat_id}.pk', 'wb') as file:
            pickle.dump(saved_data, file)

    def on_show_chatlog(self):
        """Display the chat widget and the start chat button.
    
        Called to reveal the chat interface components:
        - The chat title.
        - The chat log widget.
        - Information labels for the chat log (word and token counts).

        Generates the HTML for the chat log and hides the start inner widget.
        """
        self.title.show()
        self.generate_chat_html()
        self.log_widget.show()
        for label in self.chatlog_info_labels:
            label.show()
        self.num_of_words.show()
        self.num_of_tokens.show()
        self.start_inner_widget.hide()

    def on_hide_chatlog(self):
        """Hide the chat widget and displays the start chat button.
    
        Called to conceal the chat interface components:
        - The chat title.
        - The chat log widget.
        - Information labels for the chat log (word and token counts).
        """
        self.title.hide()
        self.log_widget.hide()
        for label in self.chatlog_info_labels:
            label.hide()
        self.num_of_words.hide()
        self.num_of_tokens.hide()
        self.start_inner_widget.show()

    def convert_markdown_to_html(self, md_text):
        """Convert Markdown text to HTML.

        Takes a string containing Markdown-formatted text and converts it to HTML
        using markdown library with specified extensions for fenced code blocks,
        syntax highlighting, and tables.

        Args:
            md_text (str): The Markdown text to be converted.

        Returns:
            str: The converted HTML representation of the Markdown text.
        """
        return markdown.markdown(
            md_text, extensions=["fenced_code", "codehilite", "tables"]
        )

    @Slot(str)
    def get_response_message_slot(self, response):
        """ Slot
        Connected to one signal:
        - controller.response_message_to_chatlog

        Handle the response message from the controller and updates the chat log.

        This method performs the following actions::
        - Enables the send button for the prompt layout.
        - Restores the cursor to its default state.
        - Converts the response message from Markdown to HTML.
        - If the current LLM is DALL-E 2 or DALL-E 3 and the response does not
          contain an error, processes the response as image URLs.
        - Sanitizes the formatted response to allow only certain HTML tags and
          attributes.
        - Appends the sanitized response to the chat log in HTML format.
        - Updates the HTML page to reflect the new AI response.

        Args:
            response (str): The response message from the API to be processed
                            and displayed.
        """
        self.prompt_layout.send_button.setEnabled(True)
        QApplication.restoreOverrideCursor()

        formatted_response = self.convert_markdown_to_html(response)
        if self.window.sidebar.current_settings.current_llm in ["DALL-E 2", "DALL-E 3"] and not "error" in response.lower():
            urls = response.split(", ")
            if len(urls) > 1:
                formatted_response = "<div class='img-grid'>" + "".join(
                    f"<div class='img-wrapper'><img src='{url}' class='img'></div>" for url in urls
                ) + "</div>"
            else:
                formatted_response = f"<div class='img-wrapper'><img src='{response}' class='img'></div>"

        allowed_tags = [
            'b', 'i', 'u', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li',
            'span', 'div', 'code', 'pre', 'table', 'tr', 'th', 'td', 'thead',
            'tbody', 'tfoot', 'caption'
        ]
        allowed_attributes = {'a': ['href', 'title']}
        sanitized_response = bleach.clean(formatted_response, tags=allowed_tags, attributes=allowed_attributes, strip=True)

        self.chat_html_logs.append(f"""
            <div class='ai-wrapper'>
                <p class='response'>{sanitized_response}</p>
            </div>
        """)
        self.generate_chat_html()

    @Slot(dict)
    def get_response_info_slot(self, response_info):
        """Slot
        Connected to one signal:
        - controller.response_info_to_chatlog

        Update the chat log information labels with response data.

        This slot receives a dictionary containing response information and 
        updates the corresponding chat log information labels. It iterates 
        through the items in the dictionary and sets the text of each label 
        to display the key-value pairs.

        Args:
            response_info (dict): A dictionary containing response information 
                                  where keys represent the label names and values
                                  represent the corresponding data.
        """
        for i, (key, value) in enumerate(response_info.items()):
            self.chatlog_info_labels[i].setText(f"{key}: {value}")

    def on_response_info_labels_reset(self):
        """Reset the chat log information labels to empty text.

        Iterates through the chat log information labels and sets their text to
        an empty string.
        """
        for label in self.chatlog_info_labels:
            label.setText("")

    def chatlog_has_text(self):
        """ Returns True if log_widget has text, else False """
        return bool(self.chat_html_logs)

    def chatlog_has_changed(self, chat_id):
        """Check if the current chat log has changed compared to the saved chat data.

        This method verifies if the chat log associated with the given `chat_id` 
        has been modified since it was last saved. It loads the saved chat data 
        from a file and compares the current chat log with the saved logs.

        Args:
            chat_id (str): The unique identifier for the chat to be checked.

        Returns:
            bool: True if the current chat log is different from the saved log, 
                  False if they are the same or if the saved data file does not exist.
        """
        file_path = f'storage/saved_data/{chat_id}.pk'
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                saved_data = pickle.load(file)
            saved_chat_html_logs = saved_data[chat_id]["chat_log"]
            return self.chat_html_logs != saved_chat_html_logs
        return True

    def get_chat_log(self):
        """Return all current chat text"""
        return self.chat_html_logs

    def on_starting_a_new_chat(self):
        """Send a signal to controller to start a new chat"""
        self.start_new_chat_to_controller.emit()


class Prompt:

    def __init__(self, chatlog):
        self.chatlog = chatlog
        self.prompt_box = CustomTextEdit(objectName="prompt_box_widget")
        self.prompt_box.textChanged.connect(self.chatlog.words_counter)
        self.prompt_box.textChanged.connect(self.chatlog.tokens_counter)

    def on_prompt_layout(self):
        """Create the layout for the prompt input area.

        This method initializes a horizontal box layout that contains a prompt
        box for user input (focused on initialization and connected to handle
        the return key press) and a send button that triggers the handling of
        the user prompt when clicked.
        """
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
        """ Get the user prompt from the prompt box and process it.

        Retrieves the text from the prompt box, stripping any leading 
        or trailing whitespace. If the `user_prompt` argument is "none", it 
        uses the text from the prompt box; otherwise, it uses the provided 
        `user_prompt`.
        
        The comparison to "none" is intentional because `on_prompt_layout`
        method connects the prompt box's return key press and the send button's
        click event to this method, passing "none" as the argument.
        This means that when the button is clicked OR the return key is pressed,
        the text from the prompt box should be processed.

        After retrieving the prompt, it clears the prompt box 
        and calls the `process_prompt` method from the chat log to handle 
        the user input.

        Args:
            user_prompt (str): An optional prompt string to be processed.
        """
        prompt = self.prompt_box.toPlainText().strip() if user_prompt == "none" else user_prompt
        self.clear_prompt_box()
        return self.chatlog.process_prompt(prompt)

    def clear_prompt_box(self):
        """Clear prompt layout"""
        self.prompt_box.clear()
        self.prompt_box.setFocus()

    def on_show_prompt_layout(self):
        """Show prompt layout and send button"""
        self.prompt_box.show()
        self.send_button.show()

    def on_hide_prompt_layout(self):
        """Hide prompt layout and send button"""
        self.prompt_box.hide()
        self.send_button.hide()
