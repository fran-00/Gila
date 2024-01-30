from PySide6.QtCore import QObject, Signal, Slot

from .openai import OpenAIClient
from .google import GoogleClient
from .cohere import CohereClient


class AIManager(QObject):
    manager_signal_to_controller = Signal(tuple)

    def __init__(self):
        super().__init__()
        self.llms = {
            "GPT-4": OpenAIClient("gpt-4"),
            "GPT-4 Turbo": OpenAIClient("gpt-4-turbo-preview"),
            "GPT-3.5 Turbo": OpenAIClient("gpt-3.5-turbo-1106"),
            "Gemini Pro": GoogleClient("gemini-pro"),
            "Cohere Chat": CohereClient(),
        }
        self.current_llm = OpenAIClient("gpt-3.5-turbo-1106")

    # def available_models(self):
    #     return list(self.llms.keys())

    def set_llm(self, current_llm):
        self.current_llm = current_llm

    @Slot(tuple)
    def handle_inbound_signal(self, data):
        new_llm = data[0]
        new_temperature = data[1]

    def handle_outbound_signal(self):
        manager_data = self.current_llm, self.current_llm.temperature
        self.manager_signal_to_controller.emit(manager_data)
