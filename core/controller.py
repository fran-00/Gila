from PySide6.QtCore import QObject, Signal, Slot


class Controller(QObject):
    user_prompt_to_model = Signal(str)
    ai_response_to_chatlog = Signal(str)
    selected_client_to_manager = Signal(str)
    current_client_to_sidebar = Signal(str)
    new_chat_started_to_model = Signal()

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
        self.view.sidebar.selected_client_to_controller.connect(self.on_change_client_from_sidebar_signal)
        self.view.sidebar.start_new_chat_to_controller.connect(self.on_start_new_chat_from_sidebar_signal)

        self.user_prompt_to_model.connect(self.model.get_user_prompt_from_controller)
        self.ai_response_to_chatlog.connect(self.view.chat.get_ai_response_from_controller)
        self.selected_client_to_manager.connect(self.model.manager.get_new_client_from_controller)
        self.current_client_to_sidebar.connect(self.view.sidebar.get_current_client_from_controller)
        self.new_chat_started_to_model.connect(self.model.new_chat_started_from_controller)

    @Slot(str)
    def on_ai_response_signal(self, ai_response):
        """Process AI response received from the MODEL and send it to CHATLOG"""
        self.ai_response_to_chatlog.emit(ai_response)

    @Slot(str)
    def on_user_prompt_signal(self, user_prompt):
        """ Process user prompt received from the CHATLOG and send it to MODEL"""
        self.user_prompt_to_model.emit(user_prompt)

    @Slot(str)
    def on_client_from_manager_signal(self, current_client):
        """Process data received from the MANAGER and send it to SIDEBAR"""
        self.current_client_to_sidebar.emit(current_client)

    @Slot(str)
    def on_change_client_from_sidebar_signal(self, new_client):
        """Process data received from the SIDEBAR and send it to MANAGER"""
        self.selected_client_to_manager.emit(new_client)

    @Slot()
    def on_start_new_chat_from_sidebar_signal(self):
        self.view.chat.chat_widget.clear()
        self.model.client.stream_stopped = True
        print("> ChatLog cleared.")
