import os

from dotenv import load_dotenv


class APIClient:

    def __init__(self, llm=None):
        self.llm = llm
        self.llm_name = None
        self.temperature = None
        self.chat_history = None
        self.api_key = None

    def check_if_api_key(self, company_name):
        """ Reads .env file to get API Key, if any """
        load_dotenv()
        if key := os.getenv(f"{company_name}_API_KEY"):
            self.api_key = key
            return True
        return False

    def get_api_key(self):
        """ Returns API Key"""
        return self.api_key

    def get_chat_history(self):
        return self.chat_history
