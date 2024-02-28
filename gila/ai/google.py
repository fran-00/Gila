import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument, GoogleAPIError

from .api_client import APIClient


class GoogleClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "GOOGLE"
        self.temperature = 0.7
        generation_config = {
            "temperature": self.temperature,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = {
            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
        }
        self.model = genai.GenerativeModel(self.llm,
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)
        self.chat_history = []
        self.chat_messages = self.model.start_chat(history=self.chat_history)

    def submit_api_key(self):
        genai.configure(api_key=self.get_api_key())

    def submit_prompt(self, prompt):
        try:
            response = self.chat_messages.send_message(prompt, stream=False)
            response_text = ""
            for chunk in response:
                response_text += chunk.text
            return True, response_text
        except GoogleAPIError as e:
            return False, e.message

    def on_chat_reset(self):
        self.chat_messages = self.model.start_chat(history=[])
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
