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

    required_files = [
        "storage/models.json",
        "storage/assets/html/about.html",
        "storage/assets/css/chatlog-styles.css",
        "storage/assets/css/spinner.css",
        "storage/assets/css/styles.css",
        "storage/assets/js/scroller.js",
    ]

    if missing_files := [f for f in required_files if not os.path.exists(f)]:
        error_msg = "The following essential files are missing:\n" + "\n".join(missing_files)
        QMessageBox.critical(None, "Critical Error", error_msg + "\nGila cannot start.")
        sys.exit(1)

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
