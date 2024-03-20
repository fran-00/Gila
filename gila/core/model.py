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
    ai_response_signal_to_controller = Signal(str)
    response_info_signal_to_controller = Signal(dict)
    start_new_chat_to_controller = Signal()
    connection_error_to_controller = Signal()
    generic_error_to_controller = Signal(str)

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
                self.start_new_chat_to_controller.emit()
                break
            ai_response = self.client.submit_prompt(self.prompt)
            no_errors = ai_response[0]
            response_message = ai_response[1]
            response_info = ai_response[2]
            if no_errors is True:
                self.ai_response_signal_to_controller.emit(response_message)
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
