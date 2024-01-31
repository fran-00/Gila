from PySide6.QtCore import QObject, Signal, Slot


class Controller(QObject):
    controller_signal_to_model = Signal(str)
    controller_signal_to_chatlog = Signal(str)

    controller_signal_to_manager_llm = Signal(str)
    controller_signal_to_sidebar_llm = Signal(str)

    def __init__(self, model, manager, chatlog, sidebar, thread):
        super().__init__()

        model.model_signal_to_controller.connect(self.on_model_signal)
        chatlog.chatlog_signal_to_controller.connect(self.on_chatlog_signal)
        manager.manager_signal_to_controller_llm.connect(self.on_manager_signal_llm)
        sidebar.sidebar_signal_to_controller_llm.connect(self.on_sidebar_signal_llm)

        self.controller_signal_to_model.connect(model.handle_inbound_signal)
        self.controller_signal_to_chatlog.connect(chatlog.handle_inbound_signal)
        self.controller_signal_to_manager_llm.connect(manager.handle_inbound_llm_signal)
        self.controller_signal_to_sidebar_llm.connect(sidebar.handle_inbound_llm_signal)

        thread.start()

    @Slot(str)
    def on_model_signal(self, data):
        """Process data received from the MODEL and send it to VIEW"""
        self.controller_signal_to_chatlog.emit(data)

    @Slot(str)
    def on_chatlog_signal(self, data):
        """ Process data received from the VIEW and send it to MODEL"""
        self.controller_signal_to_model.emit(data)

    @Slot(str)
    def on_manager_signal_llm(self, llm):
        """Process data received from the MANAGER and send it to SIDEBAR"""
        self.controller_signal_to_sidebar_llm.emit(llm)

    @Slot(str)
    def on_sidebar_signal_llm(self, llm):
        """Process data received from the SIDEBAR and send it to MANAGER"""
        self.controller_signal_to_manager_llm.emit(llm)
