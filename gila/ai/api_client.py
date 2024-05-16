import json
import random
import string


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
        with open('storage/api_keys.json', 'r') as f:
            api_keys = json.load(f)
            key = api_keys.get(f"{company_name}_API_KEY")
            if key != "None":
                self.api_key = key
                return True
            else:
                return False

    def get_api_key(self):
        """ Returns API Key"""
        return self.api_key

    def get_chat_history(self):
        return self.chat_history

    def generate_chat_id(self):
        self.chat_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
