import os
import re
import pickle

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import QObject, Signal


class StoredChats(QObject):
    loading_saved_chat_id_to_controller = Signal(str)

    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.widget_container = QWidget(objectName="stored_chats_widget")
        self.on_stored_chats_layout()

    def on_stored_chats_layout(self):
        stored_chats_layout = QVBoxLayout(self.widget_container)
        
        chats = os.listdir("storage/saved_data")
        for file in chats:
            button = QPushButton(file)
            stored_chats_layout.addWidget(button)
            button.clicked.connect(lambda: self.on_load_saved_chat(file))

    def on_load_saved_chat(self, file_name):
        """
        MUST ONLY restore chatlog, other data must be parsed directly from manager on signal receiving
        otherwise they won't fit in a single signal if sent from here
        """
        chat_id = re.sub(r'\.pk$', '', file_name)
        self.loading_saved_chat_id_to_controller.emit(chat_id)

        with open(f'storage/saved_data/{chat_id}.pk', 'rb') as file:
            saved_data = pickle.load(file)
            chat = saved_data[chat_id]
            # client = chat["client"]
            # temperature = chat["temperature"]
            # chat_history = chat["chat_history"]
            # client = chat["client"]
            chatlog = chat["chat_log"]
            print(chatlog)
