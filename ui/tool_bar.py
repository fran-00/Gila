from PySide6.QtWidgets import QToolBar, QFileDialog
from PySide6.QtGui import QAction
from PySide6.QtCore import QObject, Signal, Slot


class ToolBar(QObject):

    def __init__(self, window):
        super().__init__()
        self.window = window

    def on_toolbar(self):
        self.tb = QToolBar("Toolbar")
        save_action = QAction("&Esporta Conversazione", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip('Esporta Conversazione')
        save_action.triggered.connect(self.save_txt_file)
        self.tb.addAction(save_action)
        return self.tb

    def save_txt_file(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self.window, 'Esporta Conversazione', '.txt', '.txt', options = options)
        if file_name:
            with open(file_name, 'w') as file:
                text = self.window.chat.chat_widget.toPlainText()
                file.write(text)
