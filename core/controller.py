from PySide6.QtCore import QObject, Signal, Slot


class Controller(QObject):
    user_prompt_to_model = Signal(str)
    ai_response_to_chatlog = Signal(str)
    selected_client_to_manager = Signal(str)
    current_client_to_sidebar = Signal(str)
    new_chat_started_to_model = Signal()
    chat_stopped_to_model = Signal()
    update_status_bar = Signal(str)

    def __init__(self, model, view, thread):
        super().__init__()
        self.model = model
        self.view = view
        self.main_thread = thread
        self.connect_model()
        self.connect_view()
        self.main_thread.start()

    def connect_model(self):
        # Connect CONTROLLER's signals to MODEL's slots
        self.user_prompt_to_model.connect(self.model.get_user_prompt_slot)
        self.chat_stopped_to_model.connect(self.model.chat_stopped_slot)
        self.selected_client_to_manager.connect(self.model.manager.get_new_client_slot)

        # Connect MODEL's signals to CONTROLLER's slots
        self.model.ai_response_signal_to_controller.connect(self.ai_response_slot)
        self.model.start_new_chat_to_controller.connect(self.new_chat_started_from_model_slot)
        self.model.manager.manager_signal_to_controller_llm.connect(self.send_current_client_from_manager_slot)

    def connect_view(self):
        # Connect CONTROLLER's signals to VIEW's slots
        self.ai_response_to_chatlog.connect(self.view.chat.get_ai_response_slot)
        self.current_client_to_sidebar.connect(self.view.sidebar.get_current_client_slot)
        self.update_status_bar.connect(self.view.status_bar.on_status_update)

        # Connect VIEW's signals to CONTROLLER's slots
        self.view.sidebar.selected_client_to_controller.connect(self.client_changed_from_sidebar_slot)
        self.view.sidebar.stop_chat_to_controller.connect(self.chat_stopped_from_sidebar_slot)
        self.view.chat.user_prompt_signal_to_controller.connect(self.user_prompt_slot)
        self.view.chat.update_status_bar_from_chatlog.connect(self.view.status_bar.on_status_update)


    @Slot(str)
    def ai_response_slot(self, ai_response):
        """Receive AI response received from the MODEL and send it to CHATLOG"""
        self.ai_response_to_chatlog.emit(ai_response)
        self.update_status_bar.emit("Risposta ricevuta. In attesa di un nuovo messaggio...")

    @Slot(str)
    def user_prompt_slot(self, user_prompt):
        """ Receive user prompt received from the CHATLOG and send it to MODEL"""
        self.user_prompt_to_model.emit(user_prompt)
        self.update_status_bar.emit("Sto inviando il messaggio...")

    @Slot(str)
    def send_current_client_from_manager_slot(self, current_client):
        """Receive current client from the MANAGER and send it to SIDEBAR"""
        self.current_client_to_sidebar.emit(current_client)

    @Slot(str)
    def client_changed_from_sidebar_slot(self, new_client):
        """Receive new client name from the SIDEBAR and send it to MANAGER"""
        self.selected_client_to_manager.emit(new_client)
        self.update_status_bar.emit(f"Hai selezionato {new_client}.")

    @Slot()
    def chat_stopped_from_sidebar_slot(self):
        """Receive stopping signal from Sidebar and send it to model"""
        self.chat_stopped_to_model.emit()
        self.view.chat.chat_widget.clear()
        self.model.client.on_chat_reset()
        self.model.manager.stream_stopped = True
        self.update_status_bar.emit("La conversazione è stata chiusa.")

    @Slot()
    def new_chat_started_from_model_slot(self):
        self.model.manager.stream_stopped = False
        self.update_status_bar.emit("Nuova conversazione avviata.")
        self.main_thread.model.run()
