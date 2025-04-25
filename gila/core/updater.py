import json
import requests

from PySide6.QtCore import QObject, QThreadPool, Signal


class Updater(QObject):
    update_found_to_controller = Signal()

    def __init__(self):
        super().__init__()
        self.api_url = (
            f"https://api.github.com/repos/fran-00/gila/releases/latest"
        )

    def check_for_updates(self):
        """Check for a newer GitHub release and emit a signal if found.
        
        Fetchs latest release info from GitHub, reads the locally stored
        version, compare the two and emit update_found_to_controller signal if
        they're different.
        """
        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()
            latest = response.json()
            latest_version_tag = latest["tag_name"]
        except (requests.RequestException, KeyError, ValueError):
            return

        try:
            with open("storage/local_version.json", "r") as f:
                data = json.load(f)
            local_version_tag = data.get("local_version")
        except (IOError, ValueError):
            # If we can't read local info, assume update available
            local_version_tag = None

        if local_version_tag != latest_version_tag:
            self.update_found_to_controller.emit()

    def download_update(self):
        # TODO:
        print("downloading update...")
