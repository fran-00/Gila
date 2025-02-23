import os
import requests
import random
import string
from abc import ABC, abstractmethod

from dotenv import load_dotenv


class APIClient(ABC):

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

    def send_request(self, endpoint=None, data=None):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        if endpoint is None:
            endpoint = self._get_endpoint()
        if data is None:
            data = self.build_default_request_data()
        try:
            response = requests.post(f"{endpoint}", headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def build_default_request_data(self):
        """Creates the body of the 'data' request with default values."""
        return {
            "model": self.llm,
            "messages": self.chat_history,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

    @abstractmethod
    def _get_endpoint(self):
        """Method to implement to return the correct endpoint"""
        pass
