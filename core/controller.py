from PySide6.QtCore import QObject, Signal, Slot


class Controller(QObject):
    controller_signal_to_model = Signal(str)
    controller_signal_to_chatlog = Signal(str)

    controller_signal_to_manager_llm = Signal(str)
    controller_signal_to_sidebar_llm = Signal(str)

    def __init__(self, model, view, thread):
        super().__init__()
        self.model = model
        self.view = view
        self.connect_signals_and_slots()
        thread.start()

    def connect_signals_and_slots(self):
        self.model.model_signal_to_controller.connect(self.on_model_signal)
        self.model.manager.manager_signal_to_controller_llm.connect(self.on_manager_signal_llm)
        self.view.chat.chatlog_signal_to_controller.connect(self.on_chatlog_signal)
        self.view.sidebar.sidebar_signal_to_controller_llm.connect(self.on_sidebar_signal_llm)

        self.controller_signal_to_model.connect(self.model.handle_inbound_signal)
        self.controller_signal_to_manager_llm.connect(self.model.manager.handle_inbound_llm_signal)
        self.controller_signal_to_chatlog.connect(self.view.chat.handle_inbound_signal)
        self.controller_signal_to_sidebar_llm.connect(self.view.sidebar.handle_inbound_llm_signal)

    @Slot(str)
    def on_model_signal(self, data):
        """Process AI response received from the MODEL and send it to CHATLOG"""
        self.controller_signal_to_chatlog.emit(data)

    @Slot(str)
    def on_chatlog_signal(self, data):
        """ Process user prompt received from the CHATLOG and send it to MODEL"""
        self.controller_signal_to_model.emit(data)

    @Slot(str)
    def on_manager_signal_llm(self, llm):
        """Process data received from the MANAGER and send it to SIDEBAR"""
        self.controller_signal_to_sidebar_llm.emit(llm)

    @Slot(str)
    def on_sidebar_signal_llm(self, llm):
        """Process data received from the SIDEBAR and send it to MANAGER"""
        self.controller_signal_to_manager_llm.emit(llm)
