from PySide6.QtCore import QThread, QObject, Signal, Slot, QEventLoop


class MainThread(QThread):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        self.model.run()


class Model(QObject):
    model_signal_to_controller = Signal(str)
    player_status_signal = Signal(tuple)

    def __init__(self):
        self.client = None
        super().__init__()

    def run(self):
        self.event_loop = QEventLoop()

        while True:
            self.process_main_loop()

    def process_main_loop(self):
        self.event_loop.exec()
        ai_response = self.client.submit_prompt(self.prompt)
        self.model_signal_to_controller.emit(ai_response)

    def set_client(self, client):
        self.client = client

    @Slot(str)
    def handle_inbound_signal(self, prompt):
        self.prompt = prompt.lower()
        self.event_loop.exit()

    def handle_outbound_signal(self, ai_response):
        self.model_signal_to_controller.emit(ai_response)
