from PySide6.QtCore import QObject, QTimer, Signal, Slot

from .updater import Updater


class Controller(QObject):
    user_prompt_to_model = Signal(str)
    response_message_to_chatlog = Signal(str)
    response_info_to_chatlog = Signal(dict)
    new_settings_to_manager = Signal(str, float, int, str, str, str, int, str)
    new_chat_started_to_model = Signal()
    update_status_bar = Signal(str)
    missing_api_key_to_view = Signal(str)
    api_key_to_manager = Signal(str, str)
    api_key_is_valid_to_view = Signal(bool)
    loading_saved_chat_id_to_manager = Signal(str)

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.updater = Updater()
        self.connect_model()
        self.connect_view()
        self.connect_updater()
        QTimer.singleShot(0, self.updater.check_for_updates)

    def connect_updater(self):
        self.updater.update_found_to_controller.connect(
            self.update_found_slot
        )

    def connect_model(self):
        """Connect the controller's signals to the model's slots and vice versa.
        """
        # Connect CONTROLLER's signals to MODEL's slots
        self.user_prompt_to_model.connect(
            self.model.get_user_prompt_slot
        )
        self.new_settings_to_manager.connect(
            self.model.manager.set_new_settings_slot
        )
        self.api_key_to_manager.connect(
            self.model.manager.api_key_slot
        )
        self.loading_saved_chat_id_to_manager.connect(
            self.model.manager.restore_chat_from_id_slot
        )

        # Connect MODEL's signals to CONTROLLER's slots
        self.model.response_message_signal_to_controller.connect(
            self.response_message_slot
        )
        self.model.response_info_signal_to_controller.connect(
            self.response_info_slot
        )
        self.model.connection_error_to_controller.connect(
            self.connection_error_slot
        )
        self.model.generic_error_to_controller.connect(
            self.generic_error_slot
        )
        self.model.manager.api_key_is_valid_to_controller.connect(
            self.api_key_is_valid_slot
        )

    def connect_view(self):
        """Connect the controller's signals to the view's slots and vice versa.
        """
        # Connect CONTROLLER's signals to VIEW's slots
        self.response_message_to_chatlog.connect(
            self.view.chat.get_response_message_slot
        )
        self.response_info_to_chatlog.connect(
            self.view.chat.get_response_info_slot
        )
        self.update_status_bar.connect(
            self.view.status_bar.on_status_update_slot
        )
        self.missing_api_key_to_view.connect(
            self.view.add_api_key_modal_slot
        )
        self.api_key_is_valid_to_view.connect(
            self.view.add_api_key_modal.on_api_key_validation_slot
        )

        # Connect VIEW's signals to CONTROLLER's slots
        self.view.window_closed_signal_to_controller.connect(
            self.window_was_closed_slot
        )
        self.view.sidebar.change_settings.new_settings_to_controller.connect(
            self.settings_changed_from_sidebar_slot
        )
        self.view.sidebar.stop_chat_to_controller.connect(
            self.chat_stopped_from_sidebar_slot
        )
        self.view.sidebar.stored_chats.loading_saved_chat_id_to_controller.connect(
            self.loading_saved_chat_id_slot
        )
        self.view.chat.user_prompt_signal_to_controller.connect(
            self.user_prompt_slot
        )
        self.view.chat.start_new_chat_to_controller.connect(
            self.chat_started_slot
        )
        self.view.add_api_key_modal.api_key_to_controller.connect(
            self.api_key_from_modal_slot
        )
        self.view.update_found_modal.download_update_requested.connect(
            self.download_update_requested_slot
        )

        # Connect ChatLog to Status Bar
        self.view.chat.update_status_bar_from_chatlog.connect(
            self.view.status_bar.on_status_update_slot
        )

    @Slot(str)
    def response_message_slot(self, response_message):
        """Slot
        Connected to one signal:
        - model.response_message_signal_to_controller
        Emits:
        - response_message_to_chatlog (view.chat.get_response_message_slot)
        - update_status_bar (view.status_bar.on_status_update_slot)
        
        Handle the reception of a response from the model.

        Upon receiving an AI response, it emits the response to the chat log and
        updates the status bar to indicate that a response has been received and
        the application is waiting for a new message.

        Parameters:
            response_message (str): The AI response message to be processed.
        """
        self.response_message_to_chatlog.emit(response_message)
        self.update_status_bar.emit(
            "Response received. Waiting for a new message..."
        )

    @Slot(dict)
    def response_info_slot(self, response_info):
        """Slot
        Connected to one signal:
        - model.response_info_signal_to_controller
        Emits two signals:
        - response_info_to_chatlog (view.chat.get_response_message_slot)

        Handle the reception of response information from the model.

        Upon receiving response information, it emits the data to the sidebar
        for display.

        Parameters:
            response_info (dict): A dictionary containing information about the
                                  response, such as token usage.
        """
        self.response_info_to_chatlog.emit(response_info)

    @Slot(str)
    def user_prompt_slot(self, user_prompt):
        """Slot
        Connected to one signal:
        - view.chat.user_prompt_signal_to_controller
        Emits:
        - user_prompt_to_model (model.get_user_prompt_slot)
        - update_status_bar (view.status_bar.on_status_update_slot)

        Handle the reception of a user prompt from the chat view.

        Upon receiving a user prompt, it emits the prompt to the model for
        processing and updates the status bar to say that a new user prompt
        has been received.

        Parameters:
            user_prompt (str): The user prompt inputted in the chat.
        """
        self.user_prompt_to_model.emit(user_prompt)

    @Slot(str, float, int, str, str, str, int, str)
    def settings_changed_from_sidebar_slot(self, *args):
        """Slot
        Connected to new settings sidebar signal
        - view.sidebar.new_settings_to_controller
        Emits two signals:
        - new_settings_to_manager (model.manager.set_new_settings_slot)

        Handle the reception of new settings from the sidebar.
        Upon receiving new settings, it emits the updated settings to the model's
        manager for processing.

        Parameters:
            new_client (str): The name of the newly selected client.
            new_temperature (float): The new temperature setting for the model.
            new_max_tokens (int): The new maximum tokens setting for the model.
            new_system_message (str): The new system message for the model.
            new_image_size (str): The new image size setting.
            new_image_quality (str): The new image quality setting.
            new_image_quantity (int): The new image quantity setting.
            new_reasoning_effort (str): The new reasoning effort quantity setting.
        """
        self.new_settings_to_manager.emit(*args)

    @Slot()
    def chat_stopped_from_sidebar_slot(self):
        """Slot
        Connected to stopping signal from Sidebar:
        - view.sidebar.stop_chat_to_controller
        Saves current chat, cleans log, resets chat and emits two signals:
        - chat_stopped_to_model (model.chat_stopped_slot)
        - update_status_bar (view.status_bar.on_status_update_slot)

        Handle the stopping of a chat from the sidebar.

        When triggered, it saves the current chat if necessary, cleans the chat
        log, resets the chat state, and emits signals to indicate that the chat
        has stopped. Updates the status bar to warn that the conversation has
        been closed. The chat is saved only if there are changes in the chat log
        and there is text.
        """
        # Chat must be saved only if it's not empty and date must not be changed if chatlog is not changed
        if self.view.chat.chatlog_has_changed(self.model.manager.client.chat_id) and self.view.chat.chatlog_has_text():
            self.model.manager.save_current_chat()
            # Adds a new saved_chat_button passing chat_id as argument
            self.view.sidebar.stored_chats.add_stored_chat_button(
                self.model.manager.client.chat_id
            )
            self.view.chat.add_log_to_saved_chat_data(
                self.model.manager.client.chat_id
            )
        self.view.chat.chat_html_logs = []
        self.view.chat.generate_chat_html()
        self.model.manager.client.on_chat_reset()
        # Starts a new chat
        self.update_status_bar.emit("New conversation started.")
        self.chat_started_slot()

    @Slot()
    def chat_started_slot(self):
        """Slot
        Connected to two signals:
        - view.chat.start_new_chat_to_controller
        Checks API Key and emits two signals:
        - update_status_bar (view.status_bar.on_status_update_slot)
        - missing_api_key_to_view (view.add_api_key_modal_slot)

        Handle the event when a new chat is started.

        Checks if the API key is valid and emits signals to update the status
        bar or prompt the user for an API key if necessary. If a loaded chat is
        present, it calls the on_loaded_chat method; otherwise, it initializes
        a new chat with on_new_chat. Updates settings labels, saves current
        settings, and checks internet connectivity before starting the chat.

        If there is no internet connection, a warning modal is displayed to the
        user The UI elements related to the chat are shown or hidden based on
        the connection status.
        """
        if self.model.manager.client.is_loaded:
            self.on_loaded_chat()
        else:
            self.on_new_chat()

        # Update settings label on the sidebar
        self.view.sidebar.current_settings.update_settings_label(
            self.model.manager.on_current_settings()
        )
        # Set current settings on saved_settings.json
        self.model.manager.update_saved_settings()
        # Update settings tab values on the sidebar
        self.view.sidebar.change_settings.load_settings_from_json()
        # Update chat title
        self.view.chat.update_chat_title()
        # Set the current chat id
        self.view.sidebar.stored_chats.current_chat_id = self.model.manager.client.chat_id
        # If there is connection, start a new conversation
        if self.model.manager.check_internet_connection():
            self.model.manager.stream_stopped = False
            # Check if API Key is valid. if it is, show chatlog and run the thread
            if self.model.manager.on_api_key() is False:
                self.missing_api_key_to_view.emit(self.model.manager.client.company)
            else:
                self.view.on_show_chatlog_and_prompt_line()
                self.view.sidebar.current_settings.on_show_sidebar_settings_label()
                self.view.sidebar.on_show_sidebar_new_chat_button()
            return
        # Open a modal that warns user about the lack of connection
        self.update_status_bar.emit("No internet connection.")
        # Hide UI elements
        self.view.on_hide_chatlog_and_prompt_line()
        self.view.sidebar.on_hide_sidebar_new_chat_button()
        self.view.sidebar.current_settings.on_hide_sidebar_settings_label()
        self.view.warning_modal.on_no_internet_connection_label()
        self.view.warning_modal.exec_()

    def on_loaded_chat(self):
        self.update_status_bar.emit("Saved conversation loaded.")

    def on_new_chat(self):
        """Initialize a new chat session and updates settings if the client has
        changed.

        Called when a new conversation is started. It emits a status update
        indicating that a new conversation has begun and resets the response
        info labels in the chat view. If the user has selected a new client,
        it updates the model's client settings accordingly.

        If a new client is set, the method updates various parameters and resets
        the chat state for the new client. Finally, it sets the chat history to
        include the system message.
        """
        # Get saved response info to show them if chat is loaded
        self.view.chat.on_response_info_labels_reset()
        # Set the new client, if user has chosen a new one
        if self.model.manager.next_client:
            self.model.manager.client = self.model.manager.next_client[0]
            self.model.manager.client.llm_name = self.model.manager.next_client[1]
            self.model.manager.client.temperature = self.model.manager.next_temperature
            self.model.manager.client.max_tokens = self.model.manager.next_max_tokens
            self.model.manager.client.system_message = self.model.manager.next_system_message
            self.model.manager.client.image_size = self.model.manager.next_image_size
            self.model.manager.client.image_quality = self.model.manager.next_image_quality
            self.model.manager.client.image_quantity = self.model.manager.next_image_quantity
            self.model.manager.client.reasoning_effort = self.model.manager.next_reasoning_effort
            self.model.manager.client.on_chat_reset()
            self.model.manager.next_client = None
        # If chat is new we need to call set_chat_history to set system message
        self.model.manager.client.set_chat_history()

    @Slot(str, str)
    def api_key_from_modal_slot(self, api_key, company_name):
        """Slot
        Connected to one signal:
        - view.modal.api_key_to_controller
        Emits one signal:
        - api_key_to_manager (model.manager.api_key_slot)

        Handle the reception of an API key from the modal dialog.

        This slot is connected to the view's api_key_to_controller signal.
        It receives the API key and the associated company name. If the company
        name is provided, the method sends the API key to the model's
        manager for the specified company; otherwise, it sends the API key to
        the current client.

        Parameters:
            api_key (str): The API key to be processed.
            company_name (str): The name of the company associated with the API
                                key.
        """
        self.api_key_to_manager.emit(api_key, company_name)

    @Slot(bool)
    def api_key_is_valid_slot(self, is_key_valid):
        """Slot
        Connected to one signal:
        - model.manager.api_key_is_valid_to_controller
        Emits one signal:
        - api_key_is_valid_to_view (view.modal.on_api_key_validation_slot)

        Handle the validation status of an API key.

        Upon receiving the validation result, it emits the status to the view's
        modal for further processing, indicating whether the API key is valid
        or not.

        Parameters:
            is_key_valid (bool): A boolean indicating the validity of the API key.
        """
        self.api_key_is_valid_to_view.emit(is_key_valid)

    @Slot()
    def connection_error_slot(self):
        """Slot
        Connected to one signal:
        - model.connection_error_to_controller

        Handle the event of a connection error.

        This slot is connected to the model's connection_error_to_controller
        signal. When triggered, it emits a warning message to the chat log
        indicating that there is no internet connection, updates the status bar
        with the same message, and displays WarningLabel to inform the user
        about the connectivity issue.
        """
        self.response_message_to_chatlog.emit(
            "<span style='color:#f00'>No internet connection.</span>"
        )
        self.update_status_bar.emit("No internet connection.")
        self.view.warning_modal.on_no_internet_connection_label()
        self.view.warning_modal.exec_()

    @Slot(str)
    def generic_error_slot(self, error):
        """Slot
        Connected to one signal:
            - model.generic_error_to_controller

        Handle the event of a generic error.

        When triggered, it emits a warning message to the chat log indicating
        that an error has occurred and updates the status bar with the same message.
        WarningLabel is displayed with the provided error message to inform
        the user about the issue.

        Parameters:
            error (str): A description of the error that occurred.
        """
        self.response_message_to_chatlog.emit(
            "<span style='color:#f00'>An error has occurred! Try again!</span>"
        )
        self.update_status_bar.emit("An error has occurred.")
        self.view.warning_modal.on_label(error)
        self.view.warning_modal.exec_()

    @Slot(str)
    def loading_saved_chat_id_slot(self, chat_id):
        """Slot
        Connected to one signal:
        - view.sidebar.stored_chats.loading_saved_chat_id_to_controller

        Handle the loading of a saved chat using its chat ID.

        When triggered, it stops the current chat, sends the chat ID to the
        model's manager, updates the chat logs in the view, and emits the last
        response information to the chat log. Finally, it starts the chat with
        the loaded data.

        Parameters:
            chat_id (str): The unique identifier of the chat to be loaded.
        """
        self.chat_stopped_from_sidebar_slot()
        self.loading_saved_chat_id_to_manager.emit(chat_id)
        self.view.chat.chat_html_logs = self.view.sidebar.stored_chats.chatlog
        self.response_info_to_chatlog.emit(self.model.manager.client.last_response_info)
        self.chat_started_slot()

    @Slot()
    def window_was_closed_slot(self):
        """Slot
        Connected to one signal:
        - view.window_closed_signal_to_controller

        Handle the event when the application window is closed.

        When triggered, it checks if the chat log has any text. If it does, it
        saves the current chat and adds the log to the saved chat data.

        Notes:
            - This method ensures that any ongoing chat is saved before the
              application is closed.
        """
        if self.view.chat.chatlog_has_text():
            self.model.manager.save_current_chat()
            self.view.chat.add_log_to_saved_chat_data(self.model.manager.client.chat_id)

    @Slot()
    def update_found_slot(self):
        """Handle the event when an update is found.

        This slot is triggered when an update is detected. It emits a status bar
        update message indicating that an update has been found and displays a
        modal dialog to inform the user about the available update.

        Not yet implemented
        """
        self.update_status_bar.emit("Update found.")
        self.view.update_found_modal.exec_()

    @Slot()
    def download_update_requested_slot(self):
        """Slot
        Connected to one signal:
        - view.update_found_modal.download_update_requested
        
        Handle update download
        """
        self.updater.download_update()
