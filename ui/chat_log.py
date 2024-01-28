from PySide6.QtWidgets import QTextEdit


class ChatLog:
    def __init__(self, window):
        self.window = window
        self.chat_widget = QTextEdit()

    def on_chat_widget(self):
        self.chat_widget.setReadOnly(True)
        self.chat_widget.ensureCursorVisible()
        return self.chat_widget

    def get_chat_log(self):
        return self.chat_widget.toPlainText()
