import sys

from PySide6.QtWidgets import QApplication

from core.model import Model, MainThread
from ui.main_window import MainWindow
from core.controller import Controller
from ai.manager import AIManager


if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = AIManager()
    window = MainWindow()
    chatlog = window.chat
    sidebar = window.sidebar
    model = Model(manager)
    thread = MainThread(model)
    controller = Controller(model, manager, chatlog, sidebar, thread)
    window.show()

    sys.exit(app.exec())
