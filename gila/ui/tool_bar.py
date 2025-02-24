from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar, QFileDialog


class ToolBar(QToolBar):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.set_icons()
        self.on_save_chatlog_action()
        self.on_manage_api_keys_action()
        self.on_open_info_modal_action()

    def on_save_chatlog_action(self):
        save_action = QAction(self.save_icon, "&Export Chat", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip('Export Chat')
        save_action.triggered.connect(self.export_chatlog)
        self.addAction(save_action)

    def on_manage_api_keys_action(self):
        api_keys_action = QAction(self.key_icon, "&Manage API Keys", self)
        api_keys_action.setStatusTip('Manage API Keys')
        api_keys_action.triggered.connect(self.open_api_keys_modal)
        self.addAction(api_keys_action)

    def on_open_info_modal_action(self):
        info_action = QAction(self.info_icon, "&About Gila", self)
        info_action.setStatusTip('About Gila')
        info_action.triggered.connect(self.open_info_modal)
        self.addAction(info_action)

    def set_icons(self):
        save_icon_path = "storage/assets/icons/floppy.svg"
        self.save_icon = QIcon()
        self.save_icon.addFile(save_icon_path)
        key_icon_path = "storage/assets/icons/key.svg"
        self.key_icon = QIcon()
        self.key_icon.addFile(key_icon_path)
        settings_icon_path = "storage/assets/icons/settings.svg"
        self.settings_icon = QIcon()
        self.settings_icon.addFile(settings_icon_path)
        info_icon_path = "storage/assets/icons/info.svg"
        self.info_icon = QIcon()
        self.info_icon.addFile(info_icon_path)

    def open_change_settings_modal(self):
        self.window.sidebar.change_settings_modal.exec_()

    def open_api_keys_modal(self):
        self.window.manage_api_keys_modal.on_stored_api_keys()
        self.window.manage_api_keys_modal.update_labels()
        self.window.manage_api_keys_modal.exec_()

    def export_chatlog(self):
        # TODO:
        pass

    def save_txt(self, file_name):
        with open(file_name, "w") as file:
            text = self.window.chat.log_widget.toPlainText()
            file.write(text)

    def save_docx(self, file_name):
        # TODO:
        pass

    def save_pdf(self, file_name):
        # TODO:
        pass

    def open_info_modal(self):
        self.window.about_gila_modal.exec_()
