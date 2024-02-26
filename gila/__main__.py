import sys
import time

from PySide6.QtWidgets import QApplication

from gila.core.model import Model, MainThread
from gila.ui.view import View, LoadingScreen
from gila.core.controller import Controller
from gila.ai.manager import AIManager


def main():
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

if __name__ == "__main__":
    main()
