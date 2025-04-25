import json
import os
import requests
import sys

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot


class DownloadSignals(QObject):
    progress = Signal(int)
    finished = Signal()
    error = Signal(str)


class DownloadWorker(QRunnable):
    def __init__(self, url: str, target_path: str):
        super().__init__()
        self.url = url
        self.target_path = target_path
        self.signals = DownloadSignals()
        self.is_cancelled = False

    def cancel(self):
        self.is_cancelled = True

    @Slot()
    def run(self):
        try:
            response = requests.get(self.url, stream=True, timeout=10)
            response.raise_for_status()
            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0

            with open(self.target_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if self.is_cancelled:
                        break
                    if not chunk:
                        continue
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        percent = int(downloaded * 100 / total)
                        self.signals.progress.emit(percent)

            if self.is_cancelled:
                try:
                    os.remove(self.target_path)
                except Exception:
                    pass
                return

            self.signals.finished.emit()

        except Exception as e:
            self.signals.error.emit(str(e))


class Updater(QObject):
    update_found_to_controller = Signal(bool)
    download_progress_to_controller = Signal(int)
    download_finished_to_controller = Signal()
    download_error_to_controller = Signal(str)
    update_ready_to_install_to_controller = Signal()

    def __init__(self):
        super().__init__()
        self.api_url = f"https://api.github.com/repos/fran-00/gila/releases/latest"
        self.latest_version = None
        self.worker = None

    def check_for_updates(self, on_startup: bool = True):
        """Check for a newer GitHub release and emit a signal if found.

        Fetchs latest release info from GitHub, reads the locally stored
        version, compare the two and emit update_found_to_controller signal if
        they're different.
        """
        # Get the latest release from GitHub
        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()
            self.latest_version = response.json()
            latest_version_tag = self.latest_version["tag_name"]
        except (requests.RequestException, KeyError, ValueError):
            return

        # Read the local version
        try:
            with open("storage/local_version.json", "r") as f:
                data = json.load(f)
            local_version_tag = data.get("local_version")
        except (IOError, ValueError):
            # If can't read local info, assume update available
            local_version_tag = None

        # There is no new version, send the signal only if the user has searched
        # for updates from the toolbar
        if local_version_tag == latest_version_tag:
            if not on_startup:
                self.update_found_to_controller.emit(False)
            return

        # There is a new version: calculate zip name
        assets = self.latest_version.get("assets", [])
        zip_name = None
        for a in assets:
            nm = a.get("name", "")
            if nm.lower().endswith(".zip"):
                zip_name = nm
                break
        if not zip_name:
            zip_name = f"gila-{latest_version_tag}.zip"

        # Get executable folder path
        if getattr(sys, "frozen", False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.getcwd()
        zip_path = os.path.join(base_dir, zip_name)

        # 6) Emit a signal
        if os.path.isfile(zip_path):
            # Zip file with the update already exists
            self.update_ready_to_install_to_controller.emit()
        else:
            # Zip file is not there, ask user to download it
            self.update_found_to_controller.emit(True)

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

        self.worker = DownloadWorker(download_url, target_path)
        self.worker.signals.progress.connect(self.download_progress_to_controller)
        self.worker.signals.finished.connect(self.download_finished_to_controller)
        self.worker.signals.error.connect(self.download_error_to_controller)

        QThreadPool.globalInstance().start(self.worker)

    @Slot()
    def cancel_download_slot(self):
        """Slot
        Connected to one signal:
        - controller.cancel_download_to_updater
        """
        if self.worker:
            self.worker.cancel()

    @Slot()
    def install_update_slot(self):
        """Slot
        Connected to one signal:
        - controller.install_update_to_updater
        """
        pass
