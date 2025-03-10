import json
import re
import subprocess

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot


class WorkerSignals(QObject):
    finished = Signal(bool, str, dict)
    error = Signal(str)


class PromptWorker(QRunnable):

    def __init__(self, manager, prompt):
        super().__init__()
        self.manager = manager
        self.prompt = prompt
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """Process the assigned prompt by submitting it to the manager's client
        and emit the result through signals.

        Retrieves the client from the manager, submits the prompt for processing
        and expects a response in the format of a tuple containing:

        - A boolean indicating if there were no errors.
        - A message with the response content.
        - A dictionary with additional information about the response.

        If the processing completes successfully, the `finished` signal is
        emitted with the results. If an exception occurs during processing,
        the `error` signal is emitted with the error message.

        Raises:
            Exception: Any exceptions raised during the prompt submission are
            caught and emitted via the error signal.
        """
        try:
            client = self.manager.client
            ai_response = client.submit_prompt(self.prompt)
            no_errors, response_message, response_info = ai_response
            self.signals.finished.emit(no_errors, response_message, response_info)
        except Exception as e:
            self.signals.error.emit(str(e))


class Model(QObject):
    response_message_signal_to_controller = Signal(str)
    response_info_signal_to_controller = Signal(dict)
    connection_error_to_controller = Signal()
    generic_error_to_controller = Signal(str)
    update_found_to_controller = Signal()

    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.thread_pool = QThreadPool.globalInstance()

    @Slot(bool, str, dict)
    def handle_worker_finished(self, no_errors, response_message, response_info):
        """Handle the completion of the worker's task by processing the results
        and emitting signals to the controller.

        Parameters:
            no_errors (bool): Indicates whether the processing completed without
                              errors.
            response_message (str): The message returned from the worker, which
                                    can contain error information.
            response_info (dict): Additional information from the worker about
                                  the response.
        """
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
        """Handle the reception of the user prompt and initiates processing in
        a separate worker thread.

        Takes a user-provided prompt, creates a new worker thread, and sets up
        the prompt worker to operate within the thread.

        Parameters:
            prompt (str): The user prompt to process.
        """
        self.worker_thread = QThread()
        self.worker = PromptWorker(self.manager, prompt)
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
        """Handle errors reported by the worker by forwarding the error message
        to the controller.

        Parameters:
            error_message (str): The message detailing the error encountered during worker processing.
        """
        self.generic_error_to_controller.emit(error_message)

    def check_for_updates(self):
        """Check for updates in the GitHub repository.

        Compares the local SHA of the repository with the remote SHA
        obtained from the GitHub repository. It reads the local SHA from a JSON
        file and uses a subprocess to execute a `git ls-remote` command to fetch
        the remote SHA. If the local SHA does not match the remote SHA, it emits
        a signal indicating that an update has been found.

        Notes:
            - Not yet implemented.
        """
        repo_url = "https://github.com/fran-00/gila.git"
        with open("storage/local_sha.json", "r") as f:
            data = json.load(f)
        local_sha = data["local_sha"]
        process = subprocess.Popen(["git", "ls-remote", repo_url], stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        remote_sha = re.split(r"\t+", stdout.decode("ascii"))[0]
        process.kill()
        process.wait()
        if local_sha != remote_sha:
            self.update_found_to_controller.emit()
