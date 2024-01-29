from .openai import OpenAIClient
from .google import GoogleClient
from .cohere import CohereClient


class AIManager:

    def __init__(self):
        self.client = "GPT-3.5 Turbo"
        self.llms = {
            "GPT-4": OpenAIClient("gpt-4"),
            "GPT-4 Turbo": OpenAIClient("gpt-4-turbo-preview"),
            "GPT-3.5 Turbo": OpenAIClient("gpt-3.5-turbo-1106"),
            "Gemini Pro": GoogleClient("gemini-pro"),
            "Cohere Chat": CohereClient(),
        }

    def available_models(self):
        return list(self.llms.keys())

    def set_client(self, client):
        self.client = client
