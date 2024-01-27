from PySide6.QtCore import QObject, Signal, Slot


class Controller(QObject):
    controller_signal_to_model = Signal(str)
    controller_signal_to_view = Signal(str)

    def __init__(self, view, model, thread):
        super().__init__()

        model.model_signal_to_controller.connect(self.on_model_signal)
        view.view_signal_to_controller.connect(self.on_view_signal)
        self.controller_signal_to_model.connect(model.handle_inbound_signal)
        self.controller_signal_to_view.connect(view.handle_ai_response)

        thread.start()

    @Slot(str)
    def on_model_signal(self, data):
        """Process data received from the MODEL and send it to VIEW"""
        self.controller_signal_to_view.emit(data)

    @Slot(str)
    def on_view_signal(self, data):
        """ Process data received from the VIEW and send it to MODEL"""
        self.controller_signal_to_model.emit(data)
