import os

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class StoredChats(QWidget):
    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.setObjectName("stored_chats_widget")
        self.on_stored_chats_layout()

    def on_stored_chats_layout(self):
        stored_chats_layout = QVBoxLayout(self)
        
        chats = os.listdir("storage/saved_data")
        for file in chats:
            button = QPushButton(file)
            stored_chats_layout.addWidget(button)
