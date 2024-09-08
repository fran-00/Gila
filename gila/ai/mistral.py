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

    def submit_prompt(self, prompt):
        self.chat_history.append({"role": "user", "content": prompt})
        try:
            response = self.client.chat.complete(
                model = self.llm,
                messages = self.chat_history,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            answer = response.choices[0].message.content
            response_info = None
            self.chat_history.append({"role": "assistant", "content": answer})
            return True, answer, response_info
        except ValueError as e:
            return False, e.message, None
