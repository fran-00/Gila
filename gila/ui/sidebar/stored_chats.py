import os
import re
import pickle

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import Qt, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea

from ..modals.confirm_chat_deletion_modal import ConfirmChatDeletionModal


class StoredChats(QObject):
    loading_saved_chat_id_to_controller = Signal(str)

    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.widget_container = QWidget(objectName="stored_chats_widget")
        self.chatlog = None
        self.confirm_modal = ConfirmChatDeletionModal(self.parent_widget.window, self)
        self.chat_marked_for_deletion = None
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
        stored_chat_row = QHBoxLayout(objectName=f"{filename}_layout")
        button = QPushButton(filename, objectName=f"{filename}_button")
        button.setStyleSheet("text-align: left; padding-left: 5px;")
        delete_button = QPushButton(objectName=f"delete_button")
        delete_icon = QIcon("storage/assets/icons/trash-bin.svg")
        delete_button.setIcon(delete_icon)
        button.clicked.connect(lambda: self.on_load_saved_chat(filename))
        delete_button.clicked.connect(lambda: self.open_confirm_chat_deletion_modal(filename))
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

    def open_confirm_chat_deletion_modal(self, file_name):
        """Triggers a modal that asks to confirm before deleting """
        self.chat_marked_for_deletion = file_name
        self.confirm_modal.exec_()

    def update_chats_list(self):
        for i in reversed(range(self.stored_chats_layout.count())):
            self.stored_chats_layout.itemAt(i).layout().setParent(None)
        chats = os.listdir("storage/saved_data")
        for file in chats:
            self.add_stored_chat_button(file)

    def delete_stored_chat_by_name(self):
        layout_name = f"{self.chat_marked_for_deletion}_layout"
        for i in range(self.stored_chats_layout.layout().count()):
            layout_item = self.stored_chats_layout.layout().itemAt(i)
            if isinstance(layout_item, QHBoxLayout) and layout_item.objectName() == layout_name:
                while layout_item.count():
                    item = layout_item.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        self.delete_stored_chat_by_name(layout_item, layout_name)
                layout_item.deleteLater()
        os.remove(f"storage/saved_data/{self.chat_marked_for_deletion}")
