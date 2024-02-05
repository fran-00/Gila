import os

from dotenv import load_dotenv


class APIClient:

    def __init__(self, llm=None):
        self.llm = llm
        self.llm_name = None
        self.temperature = None
        self.chat_messages = None

    def load_api_key(self, name):
        load_dotenv()
        api_key = os.getenv(f"{name}_API_KEY")
        if api_key:
            print("API Key set")
            return api_key
        else:
            print("No API Key set")
