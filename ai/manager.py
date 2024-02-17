import json
import requests

from PySide6.QtCore import QObject, Slot, Signal

from .openai import OpenAIClient
from .google import GoogleClient
from .cohere import CohereClient


AVAILABLE_MODELS = {
        "GPT-4": OpenAIClient("gpt-4"),
        "GPT-4 Turbo": OpenAIClient("gpt-4-turbo-preview"),
        "GPT-3.5 Turbo": OpenAIClient("gpt-3.5-turbo-1106"),
        "Gemini Pro": GoogleClient("gemini-pro"),
        "Cohere Chat": CohereClient(),
}

COMPANIES = {
        "OPENAI": OpenAIClient("gpt-3.5-turbo-1106"),
        "GOOGLE": GoogleClient("gemini-pro"),
        "COHERE": CohereClient(),
}

class AIManager(QObject):
    api_key_is_valid_to_controller = Signal(bool)

    def __init__(self):
        super().__init__()
        self.client = None
        self.stream_stopped = False
        self.get_saved_settings()

    def get_saved_settings(self):
        """ Reads saved client's setting from a json file """
        with open('saved_settings.json', 'r') as f:
            data = json.load(f)
            llm_name = data.get('llm_name')
            self.client = AVAILABLE_MODELS.get(llm_name)
            self.client.llm_name = llm_name
            self.client.temperature = data.get('temperature')

    def set_new_client(self, new_llm):
        """ Takes new llm name and sets new client on call"""
        selected_llm = AVAILABLE_MODELS.get(new_llm)
        self.client = selected_llm
        self.client.llm_name = new_llm

    def on_api_key(self):
        """ Called by Controller's new_chat_started_slot, asks client to check if
        API key of the said company is present on the .env file. Returns a boolean
        with response"""
        if self.client.check_if_api_key(self.client.company) is True:
            self.client.submit_api_key()
            return True
        return False

    @Slot(str)
    def get_new_client_slot(self, new_llm):
        """ Slot
        Connected to one signal:
            - controller.selected_client_to_manager
        When triggered, calls set_new_client method with new llm name
        """
        self.set_new_client(new_llm)

    @Slot(str)
    def api_key_slot(self, api_key, company_name):
        """ Slot
        Connected to one signal:
            - controller.api_key_to_manager
        When triggered, if company_name is None, manager will send new API key
        to the current client, else it will send it on the client based on that
        company name.
        API key is then sent to client to check if is valid and emits a boolean
        signal with response. If key is valid, calls save_api_key
        """
        client = COMPANIES.get(company_name.upper())
        if client is None:
            client = AVAILABLE_MODELS.get(self.client.llm_name)
        validated = client.validate_api_key(api_key)
        if validated is True:
            self.api_key_is_valid_to_controller.emit(True)
            self.save_api_key(api_key)
        else:
            self.api_key_is_valid_to_controller.emit(False)

    def on_current_settings(self):
        """ Return current client's settings """
        settings = self.client.llm_name, self.client.temperature
        return settings

    def save_api_key(self, api_key):
        """ Saves validated API Key to .env file """
        with open('.env', 'a') as file:
            file.write(f"\n{self.client.company}_API_KEY='{api_key}'")

    def check_internet_connection(self):
        try:
            requests.head("http://www.google.com/", timeout=1)
            return True
        except requests.ConnectionError:
            return False
