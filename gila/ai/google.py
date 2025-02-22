from google import genai
from google.genai import types

from .api_client import APIClient


class GoogleClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "GOOGLE"
        self.chat_history = []

    def submit_api_key(self):
        self.client = genai.Client(api_key=self.get_api_key())
        self.chat = self.client.chats.create(model=self.llm)
        self.chat._curated_history = self.chat_history

    def submit_prompt(self, prompt):
        try:
            response = self.chat.send_message(
                message=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature,
                ),
            )
            response_info = {
                "Prompt tokens": response.usage_metadata.prompt_token_count,
                "Completion tokens": response.usage_metadata.candidates_token_count,
                "Total tokens": response.usage_metadata.total_token_count,
            }
            self.chat_history = self.chat._curated_history
            return True, response.text, response_info
        except ValueError as e:
            return False, e.message, None

    def on_chat_reset(self):
        self.chat_history = []
        self.chat_custom_name = None
        self.generate_chat_id()

    def validate_api_key(self, api_key):
        try:
            genai.Client(api_key=api_key).models.generate_content(
                model=self.llm,
                contents="test"
            )
            return True
        except genai.errors.ClientError as e:
            return False, e.message, None
