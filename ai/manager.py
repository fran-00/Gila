import json

from PySide6.QtCore import QObject, Signal, Slot

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


class AIManager(QObject):
    missing_api_key_to_controller = Signal()

    def __init__(self):
        super().__init__()
        self.client = None
        self.stream_stopped = False
        self.get_saved_settings()

    def get_saved_settings(self):
        with open('saved_settings.json', 'r') as f:
            data = json.load(f)
            llm_name = data.get('llm_name')
            self.client = AVAILABLE_MODELS.get(llm_name)
            self.client.llm_name = llm_name
            self.client.temperature = data.get('temperature')

    def set_new_client(self, new_llm):
        selected_llm = AVAILABLE_MODELS.get(new_llm)
        self.client = selected_llm
        self.client.llm_name = new_llm

    def on_api_key(self):
        if self.client.check_if_api_key(self.client.company) is True:
            self.client.submit_api_key()
            print("API KEY found")
        else:
            self.missing_api_key_to_controller.emit()

    @Slot(str)
    def get_new_client_slot(self, new_llm):
        self.set_new_client(new_llm)

    @Slot(str)
    def api_key_slot(self, api_key):
        validate = self.client.validate_api_key(api_key)
        print(validate)

    def on_current_settings(self):
        """ Return current client's settings """
        settings = self.client.llm_name, self.client.temperature
        return settings
