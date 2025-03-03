import json
import re
import subprocess

from PySide6.QtCore import QObject, QThread, Signal, Slot


class PromptWorker(QObject):
    finished = Signal(bool, str, dict)
    error = Signal(str)

    def __init__(self, manager, prompt):
        super().__init__()
        self.manager = manager
        self.prompt = prompt

    @Slot()
    def process(self):
        try:
            client = self.manager.client
            ai_response = client.submit_prompt(self.prompt)
            no_errors = ai_response[0]
            response_message = ai_response[1]
            response_info = ai_response[2]
            self.finished.emit(no_errors, response_message, response_info)
        except Exception as e:
            self.error.emit(str(e))


class Model(QObject):
    response_message_signal_to_controller = Signal(str)
    response_info_signal_to_controller = Signal(dict)
    start_chat_to_controller = Signal()
    connection_error_to_controller = Signal()
    generic_error_to_controller = Signal(str)
    update_found_to_controller = Signal()

    def __init__(self, manager):
        self.manager = manager
        super().__init__()

    @Slot(bool, str, dict)
    def handle_worker_finished(self, no_errors, response_message, response_info):
        if no_errors:
            self.response_message_signal_to_controller.emit(response_message)
            self.response_info_signal_to_controller.emit(response_info)
        else:
            if "Connection" in response_message:
                self.connection_error_to_controller.emit()
            else:
                self.generic_error_to_controller.emit(response_message)

    @Slot(str)
    def get_user_prompt_slot(self, prompt):
        self.worker_thread = QThread()
        self.worker = PromptWorker(self.manager, prompt.lower())
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.process)
        self.worker.finished.connect(self.handle_worker_finished)
        self.worker.error.connect(self.handle_worker_error)

        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.worker_thread.start()

    @Slot(str)
    def handle_worker_error(self, error_message):
        self.generic_error_to_controller.emit(error_message)

    def check_for_updates(self):
        """Check for updates in the GitHub repository.

        This method compares the local SHA of the repository with the remote SHA 
        obtained from the GitHub repository. It reads the local SHA from a JSON
        file and uses a subprocess to execute a `git ls-remote` command to fetch
        the remote SHA. If the local SHA does not match the remote SHA, it emits
        a signal indicating that an update has been found.
        
        Notes:
            - Not yet implemented.
        """
        repo_url = "https://github.com/fran-00/gila.git"
        with open('storage/local_sha.json', 'r') as f:
            data = json.load(f)
        local_sha = data["local_sha"]
        process = subprocess.Popen(["git", "ls-remote", repo_url], stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        remote_sha = re.split(r'\t+', stdout.decode('ascii'))[0]
        process.kill()
        process.wait()
        if local_sha != remote_sha:
            self.update_found_to_controller.emit()
