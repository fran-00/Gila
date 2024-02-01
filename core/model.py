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
            self.process_main_loop()

    def process_main_loop(self):
        self.event_loop.exec()
        ai_response = self.client.submit_prompt(self.prompt)
        self.ai_response_signal_to_controller.emit(ai_response)

    @Slot(str)
    def handle_user_prompt(self, prompt):
        self.prompt = prompt.lower()
        self.event_loop.exit()
