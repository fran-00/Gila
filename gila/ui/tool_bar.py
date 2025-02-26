from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar, QFileDialog

from bs4 import BeautifulSoup


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
        info_icon_path = "storage/assets/icons/info.svg"
        self.info_icon = QIcon()
        self.info_icon.addFile(info_icon_path)

    def open_api_keys_modal(self):
        self.window.manage_api_keys_modal.on_stored_api_keys()
        self.window.manage_api_keys_modal.update_labels()
        self.window.manage_api_keys_modal.exec_()

    def export_chatlog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_types = "Documento PDF (*.pdf);;File di testo (*.txt);;Documento Word (*.docx)"
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Chat", "", file_types, options=options)
        if file_name:
            if file_name.endswith(".pdf"):
                self.save_pdf(file_name)
            elif file_name.endswith(".txt"):
                self.save_txt(file_name)
            elif file_name.endswith(".docx"):
                self.save_docx(file_name)

    def save_pdf(self, file_name):
        self.window.chat.log_widget.page().printToPdf(file_name)

    def convert_html_to_text(self):
        html_content = ''.join(self.window.chat.chat_html_logs)
        soup = BeautifulSoup(html_content, "html.parser")
        prompts = soup.find_all("p", class_="prompt")
        responses = soup.find_all("p", class_="response")
        formatted_text = []
        for prompt, response in zip(prompts, responses):
            formatted_text.append(f"You: {prompt.get_text()}")
            formatted_text.append(f"Assistant: {response.get_text()}\n")
        return formatted_text

    def save_txt(self, file_name):
        with open(file_name, "w") as file:
            text = self.window.chat.log_widget.toPlainText()
            file.write(text)

    def save_docx(self, file_name):
        # TODO:
        pass

    def open_info_modal(self):
        self.window.about_gila_modal.exec_()
