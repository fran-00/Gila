import json
import os
import requests
import sys

from PySide6.QtCore import QObject, QThreadPool, Signal


class Updater(QObject):
    update_found_to_controller = Signal()

    def __init__(self):
        super().__init__()
        self.api_url = (
            f"https://api.github.com/repos/fran-00/gila/releases/latest"
        )
        self.latest_version = None

    def check_for_updates(self):
        """Check for a newer GitHub release and emit a signal if found.
        
        Fetchs latest release info from GitHub, reads the locally stored
        version, compare the two and emit update_found_to_controller signal if
        they're different.
        """
        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()
            self.latest_version = response.json()
            latest_version_tag = self.latest_version["tag_name"]
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
        assets = self.latest_version.get("assets", [])
        download_url = None
        file_name = None

        for a in assets:
            name = a.get("name", "")
            if name.lower().endswith(".zip"):
                download_url = a["browser_download_url"]
                file_name = name
                break

        if not download_url:
            download_url = self.latest_version.get("zipball_url")
            tag = self.latest_version.get("tag_name", "latest")
            file_name = f"gila-{tag}.zip"

        if getattr(sys, "frozen", False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.getcwd()

        target_path = os.path.join(base_dir, file_name)
        print(target_path)
