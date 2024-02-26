import sys
import time

from PySide6.QtWidgets import QApplication

from core.model import Model, MainThread
from ui.view import View, LoadingScreen
from core.controller import Controller
from ai.manager import AIManager


if __name__ == '__main__':
    app = QApplication(sys.argv)

    splash = LoadingScreen()
    splash.show()
    time.sleep(2)

    manager = AIManager()
    view = View()
    model = Model(manager)
    thread = MainThread(model)
    controller = Controller(model, view, thread)
    view.show()

    splash.finish(view)
    sys.exit(app.exec())
