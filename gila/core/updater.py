import json
import os
import requests
import subprocess
import sys
import tempfile
import zipfile

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
    updater_error_to_controller = Signal(str)
    update_ready_to_install_to_controller = Signal()

    def __init__(self):
        super().__init__()
        self.api_url = f"https://api.github.com/repos/fran-00/gila/releases/latest"
        self.worker = None
        self.latest_version = None
        self.asset_name = None
        self.asset_url = None
        self.zip_path = None

    def check_for_updates(self, on_startup: bool = True):
        """Check for a newer GitHub release and emit a signal if found.

        Fetchs latest release info from GitHub, reads the locally stored
        version, compare the two and emit update_found_to_controller signal if
        they're different.
        """
        # Get the latest release from GitHub
        try:
            self.latest_version = self._get_latest_release()
            latest_tag = self.latest_version["tag_name"]
            local_tag = self._read_local_version()
        except (requests.RequestException, KeyError, ValueError) as e:
            self._emit_error(f"Update check failed: {str(e)}")
            return
        except OSError as e:
            self._emit_error(f"Could not read local version: {e}")
            return

        # New update is unavailable, send the signal only if the user has searched
        # for updates from the toolbar
        if local_tag == latest_tag:
            if not on_startup:
                self.update_found_to_controller.emit(False)
            return

        # New update is available
        self.asset_name, self.asset_url = self._select_asset(
            self.latest_version.get("assets", []),
            latest_tag,
            self.latest_version.get("zipball_url")
        )
        if not self.asset_url:
            self._emit_error("No downloadable asset found for the update.")
            return

        self.zip_path = os.path.join(self._get_base_dir(), self.asset_name)

        if os.path.isfile(self.zip_path):
            # Zip file with the update already exists
            self.update_ready_to_install_to_controller.emit()
        else:
            # Zip file is not there, ask user to download it
            self.update_found_to_controller.emit(True)

    def download_update(self):
        target_path = os.path.join(self._get_base_dir(), self.asset_name)

        self.worker = DownloadWorker(self.asset_url, target_path)
        self.worker.signals.progress.connect(self.download_progress_to_controller)
        self.worker.signals.finished.connect(self.download_finished_to_controller)
        self.worker.signals.error.connect(self.updater_error_to_controller)

        QThreadPool.globalInstance().start(self.worker)

    def _get_latest_release(self):
        response = requests.get(self.api_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "tag_name" not in data:
            raise ValueError("Invalid release data: missing 'tag_name'")
        return data

    def _read_local_version(self):
        with open("storage/local_version.json", "r") as f:
            info = json.load(f)
        return info.get("local_version")

    def _select_asset(self, assets, tag, fallback_url):
        for asset in assets:
            name = asset.get("name", "")
            url  = asset.get("browser_download_url")
            if name.lower().endswith(".zip") and url:
                return name, url

        # fallback: use GitHub zipball
        if fallback_url:
            fallback_name = f"gila-{tag}.zip"
            return fallback_name, fallback_url

        return None, None

    def _get_base_dir(self):
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        return os.getcwd()

    def _emit_error(self, msg: str):
        """Emit a download/install error to the UI."""
        self.updater_error_to_controller.emit(msg)

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
        # Only Windows, for now
        if os.name != "nt":
            return self._emit_error("Automatic installation is currently only available on Windows")

        # Zip must exist
        if not self.zip_path or not os.path.isfile(self.zip_path):
            return self._emit_error("Install: zip not found.")

        try:
            # extract the executable
            tmpdir, extracted_exe = self._extract_executable_from_zip("gila.exe")
            # determine install folder and target path
            base_dir = self._get_base_dir()
            target_exe = os.path.join(base_dir, os.path.basename(extracted_exe))
            # create and run updater batch
            bat_path = self._write_update_batch(tmpdir, extracted_exe, target_exe)
            self._run_batch_and_exit(bat_path)
        except Exception as e:
            self._emit_error(f"Install error: {e}")

    def _extract_executable_from_zip(self, exe_name: str):
        tmpdir = tempfile.mkdtemp(prefix="gila_upd_")
        with zipfile.ZipFile(self.zip_path, "r") as z:
            for member in z.namelist():
                if member.lower().endswith(exe_name.lower()):
                    z.extract(member, tmpdir)
                    return tmpdir, os.path.join(tmpdir, member)
        raise FileNotFoundError(f"{exe_name} not found in {self.zip_path}")

    def _write_update_batch(self, tmpdir: str, src_exe: str, target_exe: str) -> str:
        bat_path = os.path.join(tmpdir, "updater.bat")
        script = f"""@echo off
            ping 127.0.0.1 -n 2 >nul
            copy /Y "{src_exe}" "{target_exe}" >nul
            start "" "{target_exe}"
            del "%~f0"
        """
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(script)
        return bat_path

    def _run_batch_and_exit(self, bat_path: str):
        """
        Launch the updater batch in a new console and exit current process.
        """
        subprocess.Popen(
            ["cmd", "/c", bat_path],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        sys.exit(0)
