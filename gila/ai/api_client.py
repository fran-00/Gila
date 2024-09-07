import os
import random
import string

from dotenv import load_dotenv


class APIClient:

    def __init__(self, llm=None):
        self.llm = llm
        self.llm_name = None
        self.temperature = None
        self.max_tokens = None
        self.chat_history = None
        self.api_key = None
        self.chat_id = None
        self.chat_date = None
        self.chat_custom_name = None

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

    def generate_chat_id(self):
        self.chat_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
