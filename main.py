import sys

from PySide6.QtWidgets import QApplication

from core.model import Model, MainThread
from ui.main_window import View
from core.controller import Controller
from ai.manager import AIManager


if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = AIManager()
    view = View()
    model = Model(manager)
    thread = MainThread(model)
    controller = Controller(model, view, thread)
    view.show()

    sys.exit(app.exec())
