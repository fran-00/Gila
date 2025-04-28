from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar, QFileDialog

from bs4 import BeautifulSoup
from docx import Document

from .utils import FileHandler as FH


class ToolBar(QToolBar):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self._set_icons()
        self._build_save_chatlog_action()
        self._build_manage_api_keys_action()
        self._build_update_check_action()
        self._build_open_info_modal_action()

    def _build_save_chatlog_action(self):
        save_action = QAction(self.save_icon, "&Export Chat", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip('Export Chat')
        save_action.triggered.connect(self._export_chatlog)
        self.addAction(save_action)

    def _build_manage_api_keys_action(self):
        api_keys_action = QAction(self.key_icon, "&Manage API Keys", self)
        api_keys_action.setStatusTip('Manage API Keys')
        api_keys_action.triggered.connect(self.open_api_keys_modal)
        self.addAction(api_keys_action)

    def _build_update_check_action(self):
        update_action = QAction(self.update_icon, "&Update Check", self)
        update_action.setStatusTip('Update Check')
        update_action.triggered.connect(self.update_check)
        self.addAction(update_action)

    def _build_open_info_modal_action(self):
        info_action = QAction(self.info_icon, "&About Gila", self)
        info_action.setStatusTip('About Gila')
        info_action.triggered.connect(self.open_info_modal)
        self.addAction(info_action)

    def _set_icons(self):
        save_icon_path = FH.build_asset_path("storage/assets/icons/floppy.svg")
        self.save_icon = QIcon()
        self.save_icon.addFile(save_icon_path)
        key_icon_path = FH.build_asset_path("storage/assets/icons/key.svg")
        self.key_icon = QIcon()
        self.key_icon.addFile(key_icon_path)
        update_icon_path = FH.build_asset_path("storage/assets/icons/update.svg")
        self.update_icon = QIcon()
        self.update_icon.addFile(update_icon_path)
        info_icon_path = FH.build_asset_path("storage/assets/icons/info.svg")
        self.info_icon = QIcon()
        self.info_icon.addFile(info_icon_path)

    def _export_chatlog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_types = "Text File (*.txt);;PDF Document (*.pdf);;Word Document (*.docx)"
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Chat", "", file_types, options=options)
        if file_path:
            if file_path.endswith(".pdf"):
                self._save_pdf(file_path)
            elif file_path.endswith(".txt"):
                self._save_txt(file_path)
            elif file_path.endswith(".docx"):
                self._save_docx(file_path)

    def _save_pdf(self, file_path):
        self.window.chat.log_widget.page().printToPdf(file_path)
        self.window.chat.update_status_bar_from_chatlog.emit(
            f"Chat exported as PDF to {file_path}"
        )

    def _convert_html_to_text(self):
        html_content = ''.join(self.window.chat.chat_html_logs)
        soup = BeautifulSoup(html_content, "html.parser")
        prompts = soup.find_all("p", class_="prompt")
        responses = soup.find_all("p", class_="response")
        formatted_text = []
        for prompt, response in zip(prompts, responses):
            formatted_text.append(f"You: {prompt.get_text()}")
            formatted_text.append(f"Assistant: {response.get_text()}\n")
        return formatted_text

    def _save_txt(self, file_path):
        formatted_text = self._convert_html_to_text()
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(formatted_text))
        self.window.chat.update_status_bar_from_chatlog.emit(
            f"Chat exported as TXT to {file_path}"
        )

    def _save_docx(self, file_path):
        formatted_text = self._convert_html_to_text()
        doc = Document()
        for line in formatted_text:
            doc.add_paragraph(line)
        doc.save(file_path)
        self.window.chat.update_status_bar_from_chatlog.emit(
            f"Chat exported as DOCX to {file_path}"
        )

    def open_api_keys_modal(self):
        self.window.manage_api_keys_modal.get_stored_api_keys()
        self.window.manage_api_keys_modal.update_labels()
        self.window.manage_api_keys_modal.exec_()

    def open_info_modal(self):
        self.window.about_gila_modal.exec_()

    def update_check(self):
        self.window.request_update_check_to_controller.emit()
