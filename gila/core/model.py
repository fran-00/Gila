from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot


class WorkerSignals(QObject):
    """Signals for worker threads to communicate with the main thread."""
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
        """Execute the prompt submission in a separate thread.
        
        Processes the assigned prompt by submitting it to the manager's client
        and emit the result through signals expecting a response in the format
        of a tuple containing:

        - A boolean indicating if there were no errors.
        - A message with the response content.
        - A dictionary with additional information about the response.

        If the processing completes successfully, the `finished` signal is
        emitted with the results. If an exception occurs during processing,
        the `error` signal is emitted with the error message.

        Raises:
            ConnectionError: If there is a network connection issue.
            TimeoutError: If the request times out.
            Exception: I there is an unexpected error raised during the prompt
                       submission.
        """
        try:
            client = self.manager.client
            ai_response = client.submit_prompt(self.prompt)
            no_errors, response_message, response_info = ai_response
            self.signals.finished.emit(no_errors, response_message, response_info)
        except (ConnectionError, TimeoutError) as e:
            self.signals.error.emit(f"Network error: {str(e)}")
        except Exception as e:
            import traceback
            self.signals.error.emit("Unexpected error occurred.")
            print(traceback.format_exc())


class Model(QObject):
    response_message_to_controller = Signal(str)
    response_info_to_controller = Signal(dict)
    connection_error_to_controller = Signal()
    generic_error_to_controller = Signal(str)

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
            self.response_message_to_controller.emit(response_message)
            self.response_info_to_controller.emit(response_info)
        else:
            if "Connection" in response_message:
                self.connection_error_to_controller.emit()
            else:
                self.generic_error_to_controller.emit(response_message)

    @Slot(str)
    def get_user_prompt_slot(self, prompt):
        """Handle the reception of the user prompt and initiates processing in
        a separate worker thread.

        Initialize a PromptWorker with the provided prompt and connects its
        signals to the corresponding slot methods for handling the results and
        errors. The worker is then started in the thread pool.

        Parameters:
            prompt (str): The user prompt to process.
        """
        worker = PromptWorker(self.manager, prompt)
        worker.signals.finished.connect(self.handle_worker_finished)
        worker.signals.error.connect(self.handle_worker_error)
        self.thread_pool.start(worker)

    @Slot(str)
    def handle_worker_error(self, error_message):
        """Handle errors reported by the worker by forwarding the error message
        to the controller.

        Parameters:
            error_message (str): The message detailing the error encountered during worker processing.
        """
        self.generic_error_to_controller.emit(error_message)
