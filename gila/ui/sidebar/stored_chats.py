import os
import re
import pickle

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import Qt, QIcon
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QScrollArea, QLabel)

from ..modals.rename_chat_modal import RenameChatModal
from ..modals.confirm_chat_deletion_modal import ConfirmChatDeletionModal


class StoredChats(QObject):
    loading_saved_chat_id_to_controller = Signal(str)

    def __init__(self, parent_class):
        super().__init__()
        self.parent_class = parent_class
        self.widget_container = QWidget(objectName="stored_chats_widget")
        self.chatlog = None
        self.current_chat_id = None
        self.rename_modal = RenameChatModal(self.parent_class.window, self)
        self.confirm_modal = ConfirmChatDeletionModal(self.parent_class.window, self)
        self.chat_marked_for_renaming = None
        self.chat_marked_for_deletion = None
        self.on_stored_chats_layout()

    def on_stored_chats_layout(self):
        self.stored_chats_layout = QVBoxLayout(self.widget_container)
        self.stored_chats_layout.setAlignment(Qt.Alignment.AlignTop)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.widget_container)
        self.scroll_area.setWidgetResizable(True)
        self.create_chats_list()

    def add_stored_chat_button(self, chat_id, custom_name=None):
        """ Adds an horizzontal layout with a button to delete a stored chat,
            a button to rename it and a button to delete it
        """
        # If this chat is already saved, skips button's creation
        if same_name_button := self.widget_container.findChild(QPushButton, f"{chat_id}_button"):
            return
        stored_chat_row = QHBoxLayout(objectName=f"{chat_id}_layout")
        if custom_name is not None:
            button = QPushButton(custom_name, objectName=f"{chat_id}_button")
        else:
            button = QPushButton(chat_id, objectName=f"{chat_id}_button")
        button.setStyleSheet("text-align: left; padding-left: 5px;")
        rename_button = QPushButton(objectName=f"rename_button")
        rename_icon = QIcon("storage/assets/icons/pen.svg")
        rename_button.setIcon(rename_icon)
        rename_button.clicked.connect(lambda: self.open_rename_chat_modal(chat_id))
        delete_button = QPushButton(objectName=f"delete_button")
        delete_icon = QIcon("storage/assets/icons/trash-bin.svg")
        delete_button.setIcon(delete_icon)
        button.clicked.connect(lambda: self.on_load_saved_chat(chat_id))
        delete_button.clicked.connect(lambda: self.open_confirm_chat_deletion_modal(chat_id))
        stored_chat_row.addWidget(button, 8)
        stored_chat_row.addWidget(rename_button, 1)
        stored_chat_row.addWidget(delete_button, 1)
        self.stored_chats_layout.insertLayout(0, stored_chat_row)

    def on_load_saved_chat(self, chat_id):
        """ MUST ONLY restore chatlog, other data must be parsed directly from manager on signal receiving
            otherwise they won't fit in a single signal if sent from here
        """
        # Checks if requested chat is already open. If so, ignores the loading
        if chat_id != self.current_chat_id:
            with open(f'storage/saved_data/{chat_id}.pk', 'rb') as file:
                saved_data = pickle.load(file)
                chat = saved_data[chat_id]
                self.chatlog = chat["chat_log"]
            self.current_chat_id = chat_id
            self.loading_saved_chat_id_to_controller.emit(chat_id)

    def open_confirm_chat_deletion_modal(self, chat_id):
        """Triggers a modal that asks to confirm before deleting """
        self.chat_marked_for_deletion = chat_id
        if self.chat_marked_for_deletion == self.current_chat_id:
            self.parent_class.window.warning_modal.on_deleting_current_chat_label()
            self.parent_class.window.warning_modal.exec_()
            return
        self.confirm_modal.exec_()

    def rename_stored_chat(self, new_name):
        """ Updates text shown on saved chat button """
        self.rename_modal.new_name_entry.clear()
        button = self.widget_container.findChild(QPushButton, f"{self.chat_marked_for_renaming}_button")
        button.setText(new_name)
        with open(f'storage/saved_data/{self.chat_marked_for_renaming}.pk', 'rb') as file:
            saved_data = pickle.load(file)
        saved_data[self.chat_marked_for_renaming]["chat_custom_name"] = new_name
        with open(f'storage/saved_data/{self.chat_marked_for_renaming}.pk', 'wb') as file:
            pickle.dump(saved_data, file)

    def create_chats_list(self):
        chats = os.listdir("storage/saved_data")
        # Create a list of tuples (file, data_creazione)
        chat_files_with_dates = []
        for chat_file in chats:
            chat_id = re.sub(r'\.pk$', '', chat_file)
            with open(f'storage/saved_data/{chat_file}', 'rb') as file:
                saved_data = pickle.load(file)
            chat_date = saved_data[chat_id]["chat_date"]
            chat_files_with_dates.append((chat_file, chat_date))
        # Sorts the list based on file creation date
        chat_files_with_dates.sort(key=lambda x: x[1], reverse=True)
        # Calls add_stored_chat_button based on stored chats order
        for chat_file, _ in chat_files_with_dates:
            chat_id = re.sub(r'\.pk$', '', chat_file)
            with open(f'storage/saved_data/{chat_file}', 'rb') as file:
                saved_data = pickle.load(file)
            custom_name = saved_data[chat_id]["chat_custom_name"]
            self.add_stored_chat_button(chat_id, custom_name)

    def open_rename_chat_modal(self, chat_id):
        """Triggers a modal that asks to insert a new name for the chat """
        self.chat_marked_for_renaming = chat_id
        self.rename_modal.exec_()

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
        os.remove(f"storage/saved_data/{self.chat_marked_for_deletion}.pk")
