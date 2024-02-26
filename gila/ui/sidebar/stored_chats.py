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
        self.chatlog = None
        self.on_stored_chats_layout()

    def on_stored_chats_layout(self):
        self.stored_chats_layout = QVBoxLayout(self.widget_container)
        
        chats = os.listdir("storage/saved_data")
        for file in chats:
            self.add_stored_chat_button(file)

    def add_stored_chat_button(self, filename):
        button = QPushButton(filename, objectName=f"{filename}_button")
        button.clicked.connect(lambda: self.on_load_saved_chat(filename))
        self.stored_chats_layout.addWidget(button)

    def on_load_saved_chat(self, file_name):
        """
        MUST ONLY restore chatlog, other data must be parsed directly from manager on signal receiving
        otherwise they won't fit in a single signal if sent from here
        """
        chat_id = re.sub(r'\.pk$', '', file_name)
        with open(f'storage/saved_data/{chat_id}.pk', 'rb') as file:
            saved_data = pickle.load(file)
            chat = saved_data[chat_id]
            self.chatlog = chat["chat_log"]
        self.loading_saved_chat_id_to_controller.emit(chat_id)
