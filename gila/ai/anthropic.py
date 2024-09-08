import anthropic
from .api_client import APIClient


class AnthropicClient(APIClient):
    
    def __init__(self, llm):
        super().__init__(llm)
        self.company = "ANTHROPIC"
        self.chat_history = []

