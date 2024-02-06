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

    def __init__(self):
        super().__init__()
        self.client = None
        self.stream_stopped = False

    def available_models(self):
        """ TODO: must check API keys """
        pass

    def set_new_client(self, new_llm):
        selected_llm = self.llms.get(new_llm)
        self.client = selected_llm
        self.client.llm_name = new_llm

    @Slot(str)
    def get_new_client_slot(self, new_llm):
        self.set_new_client(new_llm)

    def on_current_settings(self):
        """ Return current client's settings """
        settings = self.client.llm_name, self.client.temperature
        return settings
