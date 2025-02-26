import json
import re
import subprocess

from PySide6.QtCore import QThread, QObject, Signal, Slot, QEventLoop


class MainThread(QThread):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        self.model.run()

    def stop(self):
        self.model.stop()


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
        self.running = False

    def run(self):
        self.event_loop = QEventLoop()
        self.client = self.manager.client

        while self.running:
            self.event_loop.exec()
            if not self.running:
                break
            if self.manager.stream_stopped is True:
                self.start_chat_to_controller.emit()
                break
            self.handle_client_response()

    def handle_client_response(self):
        ai_response = self.client.submit_prompt(self.prompt)
        no_errors = ai_response[0]
        response_message = ai_response[1]
        response_info = ai_response[2]
        if no_errors is True:
            self.response_message_signal_to_controller.emit(response_message)
            self.response_info_signal_to_controller.emit(response_info)
        elif no_errors is False:
            if "Connection" in response_message:
                self.connection_error_to_controller.emit()
            else:
                self.generic_error_to_controller.emit(response_message)

    def stop(self):
        self.event_loop.exit()

    @Slot(str)
    def get_user_prompt_slot(self, prompt):
        """ Slot
        Connected to one signal:
            - controller.user_prompt_to_model
        Gets user prompt and stops event loop.
        """
        self.prompt = prompt.lower()
        self.event_loop.exit()

    def check_for_updates(self):
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
