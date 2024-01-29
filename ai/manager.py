from PySide6.QtCore import QObject, Signal, Slot

from .openai import OpenAIClient
from .google import GoogleClient
from .cohere import CohereClient


class AIManager(QObject):
    manager_signal_to_controller = Signal(tuple)

    def __init__(self):
        super().__init__()
        self.client = OpenAIClient("gpt-3.5-turbo-1106")
        self.llms = {
            "GPT-4": OpenAIClient("gpt-4"),
            "GPT-4 Turbo": OpenAIClient("gpt-4-turbo-preview"),
            "GPT-3.5 Turbo": OpenAIClient("gpt-3.5-turbo-1106"),
            "Gemini Pro": GoogleClient("gemini-pro"),
            "Cohere Chat": CohereClient(),
        }
        

    # def available_models(self):
    #     return list(self.llms.keys())

    def set_client(self, client):
        self.client = client

    @Slot(tuple)
    def handle_inbound_signal(self):
        self.manager_signal_to_controller.emit(list(self.llms.keys()))
