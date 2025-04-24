from PySide6.QtCore import QObject, Signal


class Updater(QObject):
    update_found_to_controller = Signal()

    def __init__(self):
        super().__init__()
        self.api_url = (
            f"https://api.github.com/repos/fran-00/gila/releases/latest"
        )
