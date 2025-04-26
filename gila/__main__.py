import sys
import os
import time

from PySide6.QtWidgets import QApplication, QMessageBox

from gila.core.model import Model
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
    controller = Controller(model, view)
    view.show()

    splash.finish(view)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
