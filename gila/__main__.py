import sys

from PySide6.QtWidgets import QApplication

from gila.core.model import Model
from gila.ui.view import View
from gila.core.controller import Controller
from gila.ai.manager import AIManager


def main():
    app = QApplication(sys.argv)

    if getattr(sys, 'frozen', False):
        try:
            import pyi_splash # type: ignore
        except ModuleNotFoundError:
            pass


    manager = AIManager()
    view = View()
    model = Model(manager)
    controller = Controller(model, view)
    view.show()

    try:
        pyi_splash.close()
    except NameError:
        pass

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
