from PySide6.QtCore import QObject, Signal, Slot


class Controller(QObject):
    user_prompt_to_model = Signal(str)
    ai_response_to_chatlog = Signal(str)

    controller_signal_to_manager_llm = Signal(str)
    controller_signal_to_sidebar_llm = Signal(str)

    def __init__(self, model, view, thread):
        super().__init__()
        self.model = model
        self.view = view
        self.connect_signals_and_slots()
        thread.start()

    def connect_signals_and_slots(self):
        self.model.ai_response_signal_to_controller.connect(self.on_ai_response_signal)
        self.view.chat.user_prompt_signal_to_controller.connect(self.on_user_prompt_signal)
        self.model.manager.manager_signal_to_controller_llm.connect(self.on_client_from_manager_signal)
        self.view.sidebar.sidebar_signal_to_controller_llm.connect(self.on_change_client_from_sidebar_signal)

        self.user_prompt_to_model.connect(self.model.handle_user_prompt)
        self.ai_response_to_chatlog.connect(self.view.chat.handle_ai_response)
        self.controller_signal_to_manager_llm.connect(self.model.manager.handle_inbound_llm_signal)
        self.controller_signal_to_sidebar_llm.connect(self.view.sidebar.handle_inbound_llm_signal)

    @Slot(str)
    def on_ai_response_signal(self, ai_response):
        """Process AI response received from the MODEL and send it to CHATLOG"""
        self.ai_response_to_chatlog.emit(ai_response)

    @Slot(str)
    def on_user_prompt_signal(self, user_prompt):
        """ Process user prompt received from the CHATLOG and send it to MODEL"""
        self.user_prompt_to_model.emit(user_prompt)

    @Slot(str)
    def on_client_from_manager_signal(self, llm):
        """Process data received from the MANAGER and send it to SIDEBAR"""
        self.controller_signal_to_sidebar_llm.emit(llm)

    @Slot(str)
    def on_change_client_from_sidebar_signal(self, llm):
        """Process data received from the SIDEBAR and send it to MANAGER"""
        self.controller_signal_to_manager_llm.emit(llm)
