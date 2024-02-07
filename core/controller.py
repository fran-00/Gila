from PySide6.QtCore import QObject, Signal, Slot


class Controller(QObject):
    user_prompt_to_model = Signal(str)
    ai_response_to_chatlog = Signal(str)
    selected_client_to_manager = Signal(str)
    new_chat_started_to_model = Signal()
    chat_stopped_to_model = Signal()
    update_status_bar = Signal(str)
    missing_api_key_to_view = Signal()
    api_key_to_manager = Signal(str)
    api_key_is_valid_to_view = Signal(bool)

    def __init__(self, model, view, thread):
        super().__init__()
        self.model = model
        self.view = view
        self.main_thread = thread
        self.connect_model()
        self.connect_view()

    def connect_model(self):
        # Connect CONTROLLER's signals to MODEL's slots
        self.user_prompt_to_model.connect(self.model.get_user_prompt_slot)
        self.chat_stopped_to_model.connect(self.model.chat_stopped_slot)
        self.selected_client_to_manager.connect(self.model.manager.get_new_client_slot)
        self.api_key_to_manager.connect(self.model.manager.api_key_slot)

        # Connect MODEL's signals to CONTROLLER's slots
        self.model.ai_response_signal_to_controller.connect(self.ai_response_slot)
        self.model.start_new_chat_to_controller.connect(self.new_chat_started_slot)
        self.model.manager.api_key_is_valid_to_controller.connect(self.api_key_is_valid_slot)

    def connect_view(self):
        # Connect CONTROLLER's signals to VIEW's slots
        self.ai_response_to_chatlog.connect(self.view.chat.get_ai_response_slot)
        self.update_status_bar.connect(self.view.status_bar.on_status_update_slot)
        self.missing_api_key_to_view.connect(self.view.on_missing_key_modal_slot)
        self.api_key_is_valid_to_view.connect(self.view.modal.on_api_key_validation_slot)

        # Connect VIEW's signals to CONTROLLER's slots
        self.view.sidebar.selected_client_to_controller.connect(self.client_changed_from_sidebar_slot)
        self.view.sidebar.stop_chat_to_controller.connect(self.chat_stopped_from_sidebar_slot)
        self.view.chat.user_prompt_signal_to_controller.connect(self.user_prompt_slot)
        self.view.chat.start_new_chat_to_controller.connect(self.new_chat_started_slot)
        self.view.modal.api_key_to_controller.connect(self.api_key_from_modal_slot)
        
        # Connect ChatLog to Status Bar
        self.view.chat.update_status_bar_from_chatlog.connect(self.view.status_bar.on_status_update_slot)


    @Slot(str)
    def ai_response_slot(self, ai_response):
        """ Slot
        Connected to one signal:
            - model.ai_response_signal_to_controller
        Emits two signals:
            - ai_response_to_chatlog (view.chat.get_ai_response_slot)
            - update_status_bar (view.status_bar.on_status_update_slot)
        
        Receive AI response from the MODEL and send it to CHATLOG
        """
        self.ai_response_to_chatlog.emit(ai_response)
        self.update_status_bar.emit("Risposta ricevuta. In attesa di un nuovo messaggio...")

    @Slot(str)
    def user_prompt_slot(self, user_prompt):
        """ Slot
        Connected to one signal:
            - view.chat.user_prompt_signal_to_controller
        Emits two signals:
            - user_prompt_to_model (model.get_user_prompt_slot)
            - update_status_bar (view.status_bar.on_status_update_slot)
        """
        self.user_prompt_to_model.emit(user_prompt)
        self.update_status_bar.emit("Sto inviando il messaggio...")

    @Slot(str)
    def client_changed_from_sidebar_slot(self, new_client):
        """ Slot
        Connected to new client sidebar signal
            - view.sidebar.selected_client_to_controller
        Emits two signals:
            - selected_client_to_manager (model.manager.get_new_client_slot)
            - update_status_bar (view.status_bar.on_status_update_slot)
        """
        self.selected_client_to_manager.emit(new_client)
        self.update_status_bar.emit(f"Hai selezionato {new_client}.")

    @Slot()
    def chat_stopped_from_sidebar_slot(self):
        """ Slot
        Connected to stopping signal from Sidebar:
            - view.sidebar.stop_chat_to_controller
        Cleans log, resets chat and emits two signals:
            - chat_stopped_to_model (model.chat_stopped_slot)
            - update_status_bar (view.status_bar.on_status_update_slot)
        """
        self.chat_stopped_to_model.emit()
        self.view.chat.chat_widget.clear()
        self.model.client.on_chat_reset()
        self.model.manager.stream_stopped = True
        self.update_status_bar.emit("La conversazione è stata chiusa.")

    @Slot()
    def new_chat_started_slot(self):
        """ Slot
        Connected to two signals:
            - view.chat.start_new_chat_to_controller
            - model.start_new_chat_to_controller
        Checks API Key and emits two signals:
            - update_status_bar (view.status_bar.on_status_update_slot)
            - missing_api_key_to_view (view.on_missing_key_modal_slot)
        """
        self.model.manager.stream_stopped = False
        self.update_status_bar.emit("Nuova conversazione avviata.")
        self.view.sidebar.update_settings_label(self.model.manager.on_current_settings())
        if self.model.manager.on_api_key() is False:
            self.missing_api_key_to_view.emit()
        else:
            self.view.on_show_chatlog_and_prompt_line()
            self.view.sidebar.on_show_widgets()
        self.main_thread.model.run()

    @Slot(str)
    def api_key_from_modal_slot(self, api_key):
        """ Slot
        Connected to one signal:
            - view.modal.api_key_to_controller
        Emits one signal:
            - api_key_to_manager (model.manager.api_key_slot)
        """
        self.api_key_to_manager.emit(api_key)

    @Slot(bool)
    def api_key_is_valid_slot(self, is_key_valid):
        """ Slot
        Connected to one signal:
            - model.manager.api_key_is_valid_to_controller
        Emits one signal:
            - api_key_is_valid_to_view (view.modal.on_api_key_validation_slot)
        """
        self.api_key_is_valid_to_view.emit(is_key_valid)
