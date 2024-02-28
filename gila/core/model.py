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
            print("> API response received!")
            if ai_response[0] is True:
                self.ai_response_signal_to_controller.emit(ai_response[1])
            elif ai_response[0] is False:
                if "Connection" in ai_response[1]:
                    self.connection_error_to_controller.emit()
                else:
                    self.generic_error_to_controller.emit(ai_response[1])

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
        print("> Processing user prompt and waiting for API Response...")
        self.event_loop.exit()
