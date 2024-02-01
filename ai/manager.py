from PySide6.QtCore import QObject, Signal, Slot

from .openai import OpenAIClient
from .google import GoogleClient
from .cohere import CohereClient


class AIManager(QObject):
    manager_signal_to_controller_llm = Signal(tuple)

    def __init__(self):
        super().__init__()
        self.llms = {
            "GPT-4": OpenAIClient("gpt-4"),
            "GPT-4 Turbo": OpenAIClient("gpt-4-turbo-preview"),
            "GPT-3.5 Turbo": OpenAIClient("gpt-3.5-turbo-1106"),
            "Gemini Pro": GoogleClient("gemini-pro"),
            "Cohere Chat": CohereClient(),
        }
        self.client = OpenAIClient("gpt-3.5-turbo-1106")
        self.client.llm_name = "GPT-3.5 Turbo"

    def available_models(self):
        """ TODO: must check API keys """
        pass

    def set_new_client(self, new_llm):
        selected_llm = self.llms.get(new_llm)
        self.client = selected_llm
        self.client.llm_name = new_llm

    @Slot(str)
    def get_new_client_from_controller(self, new_llm):
        self.set_new_client(new_llm)

    def send_current_client_to_controller(self):
        """ """
        self.manager_signal_to_controller_llm.emit(self.client.llm_name)
