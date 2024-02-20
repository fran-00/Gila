import os

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import QObject


class StoredChats(QObject):
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
