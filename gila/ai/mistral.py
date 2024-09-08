import os

from mistralai import Mistral
from .api_client import APIClient


class MistralClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "MISTRAL"
        self.chat_history = []

    def submit_api_key(self):
        self.client = Mistral(api_key=self.get_api_key())
