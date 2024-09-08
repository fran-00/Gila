import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument, GoogleAPIError

from .api_client import APIClient


class GoogleClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "GOOGLE"
        self.model = genai.GenerativeModel(self.llm)
        self.chat_history = []
        self.chat_messages = self.model.start_chat(history=self.chat_history)

    def submit_api_key(self):
        genai.configure(api_key=self.get_api_key())

    def submit_prompt(self, prompt):
        try:
            response = self.chat_messages.send_message(prompt, stream=False)
            response_text = "".join(chunk.text for chunk in response)
            response_info = {"total_tokens": self.model.count_tokens(self.chat_history)}
            return True, response_text, response_info
        except GoogleAPIError as e:
            return False, e.message, None

    def on_chat_reset(self):
        self.chat_messages = self.model.start_chat(history=[])
        self.chat_custom_name = None
        self.generate_chat_id()

    def validate_api_key(self, api_key):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        try:
            model.generate_content("test")
            return True
        except InvalidArgument as e:
            print(e)
            return False
