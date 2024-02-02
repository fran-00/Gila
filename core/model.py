from PySide6.QtCore import QThread, QObject, Signal, Slot, QEventLoop


class MainThread(QThread):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        self.model.run()


class Model(QObject):
    ai_response_signal_to_controller = Signal(str)

    def __init__(self, manager):
        self.manager = manager
        self.client = self.manager.client
        super().__init__()

    def run(self):
        self.event_loop = QEventLoop()
        self.manager.send_current_client_to_controller()

        while True:
            self.event_loop.exec()
            if self.manager.stream_stopped is True:
                break
            ai_response = self.client.submit_prompt(self.prompt)
            print("> API response received!")
            self.ai_response_signal_to_controller.emit(ai_response)

    @Slot(str)
    def get_user_prompt_from_controller(self, prompt):
        self.prompt = prompt.lower()
        print("> Processing user prompt and waiting for API Response...")
        self.event_loop.exit()

    @Slot()
    def chat_stopped_from_controller(self):
        print("> Main loop was stopped.")
        self.event_loop.exit()

    @Slot()
    def new_chat_started_from_controller(self):
        pass
