from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar, QFileDialog

from docx import Document
from reportlab.pdfgen.canvas import Canvas


class ToolBar(QToolBar):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.set_icons()
        self.on_save_chatlog_action()
        self.on_manage_api_keys_action()
        self.on_chat_settings_action()
        self.on_open_info_modal_action()

    def on_save_chatlog_action(self):
        save_action = QAction(self.save_icon, "&Esporta Conversazione", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip('Esporta Conversazione')
        save_action.triggered.connect(self.export_chatlog)
        self.addAction(save_action)

    def on_manage_api_keys_action(self):
        api_keys_action = QAction(self.key_icon, "&Gestisci Chiavi API", self)
        api_keys_action.setStatusTip('Gestisci Chiavi API')
        api_keys_action.triggered.connect(self.open_api_keys_modal)
        self.addAction(api_keys_action)

    def on_chat_settings_action(self):
        chat_settings_action = QAction(self.settings_icon, "&Modifica Impostazioni Chat", self)
        chat_settings_action.setStatusTip('Modifica Impostazioni Chat')
        chat_settings_action.triggered.connect(self.open_change_settings_modal)
        self.addAction(chat_settings_action)

    def on_open_info_modal_action(self):
        info_action = QAction(self.info_icon, "&Informazioni", self)
        info_action.setStatusTip('Informazioni')
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

    def open_change_settings_modal(self):
        self.window.sidebar.change_settings_modal.exec_()

    def open_api_keys_modal(self):
        self.window.manage_api_keys_modal.on_stored_api_keys()
        self.window.manage_api_keys_modal.update_labels()
        self.window.manage_api_keys_modal.exec_()

    def export_chatlog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_types = "File di testo (*.txt);;Documento Word (*.docx);;Documento PDF (*.pdf)"
        file_name, _ = QFileDialog.getSaveFileName(self, "Esporta Conversazione", "", file_types, options=options)
        if file_name:
            if file_name.endswith(".txt"):
                self.save_txt(file_name)
            elif file_name.endswith(".docx"):
                self.save_docx(file_name)
            elif file_name.endswith(".pdf"):
                self.save_pdf(file_name)

    def save_txt(self, file_name):
        with open(file_name, "w") as file:
            text = self.window.chat.log_widget.toPlainText()
            file.write(text)

    def save_docx(self, file_name):
        document = Document()
        text = self.window.chat.log_widget.toPlainText()
        document.add_paragraph(text)
        document.save(file_name)

    def save_pdf(self, file_name):
        # FIXME: è tutto storto, sistemalo
        text = self.window.chat.log_widget.toPlainText()
        canvas = Canvas(file_name)
        canvas.setFont("Times-Roman", 12)
        canvas.drawString(100, 750, text)
        canvas.save()

    def open_info_modal(self):
        print("Info Modal Called!")
