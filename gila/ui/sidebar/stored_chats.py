import os
import re
import pickle

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea


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
        self.stored_chats_layout.setAlignment(Qt.Alignment.AlignTop)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.widget_container)
        self.scroll_area.setWidgetResizable(True)
        self.update_chats_list()

    def add_stored_chat_button(self, filename):
        """ Adds an horizzontal layout with a chat button and a button to delete
            that chat
        """
        stored_chat_row = QHBoxLayout()
        button = QPushButton(filename, objectName=f"{filename}_button")
        delete_button = QPushButton("X", objectName=f"{filename}_delete_button")
        button.clicked.connect(lambda: self.on_load_saved_chat(filename))
        delete_button.clicked.connect(lambda: self.on_delete_saved_chat(filename))
        stored_chat_row.addWidget(button, 9)
        stored_chat_row.addWidget(delete_button, 1)
        self.stored_chats_layout.addLayout(stored_chat_row)

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

    def on_delete_saved_chat(self, file_name):
        print(f"DELETE button for {file_name} was pressed")

    def update_chats_list(self):
        for i in reversed(range(self.stored_chats_layout.count())): 
            self.stored_chats_layout.itemAt(i).widget().setParent(None)
        chats = os.listdir("storage/saved_data")
        for file in chats:
            self.add_stored_chat_button(file)

    def delete_stored_chat_by_name(self, name):
        for child in self.stored_chats_layout.findChildren(QHBoxLayout):
            if child.objectName() == name:
                child.deleteLater()
                return
