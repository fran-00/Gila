import sys
import os
import time

from PySide6.QtWidgets import QApplication

from gila.core.model import Model
from gila.ui.view import View
from gila.core.controller import Controller
from gila.ai.manager import AIManager


def main():
    app = QApplication(sys.argv)

    manager = AIManager()
    view = View()
    model = Model(manager)
    controller = Controller(model, view)
    view.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
