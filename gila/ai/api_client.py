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

    def send_request(self, headers=None, endpoint=None, data=None):
        endpoint = endpoint or self._get_endpoint()
        headers = headers or self.build_default_request_headers()
        data = data or self.build_default_request_data()
        try:
            response = requests.post(f"{endpoint}", headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def build_default_request_headers(self):
        """Creates request headers with default values."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def build_default_request_data(self):
        """Creates request data with default values."""
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

    @abstractmethod
    def _extract_response_data(self, response):
        """Method to implement in subclasses to extract ai_response and response_info."""
        pass

    def validate_api_key(self, api_key):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": self.llm,
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": 5,
        }
        response = self.send_request(headers=headers, data=data)
        return False if "error" in response else True

    def submit_prompt(self, prompt):
        """Handles prompt submission."""
        self.chat_history.append(self._format_user_message(prompt))

        # Get request parameters (allows overrides for specific clients)
        params = self._get_request_params()

        try:
            response = self.send_request(**params)
            ai_response, response_info = self._extract_response_data(response)
            self.chat_history.append(self._format_ai_message(ai_response))

            return True, ai_response, response_info
        except KeyError as e:
            return False, str(e), None

    def _format_user_message(self, prompt):
        """Defines how the user message should be formatted. Override if needed."""
        return {"role": "user", "content": prompt}

    def _format_ai_message(self, ai_response):
        """Defines how the AI response should be formatted. Override if needed."""
        return {"role": "assistant", "content": ai_response}

    def _get_request_params(self):
        """Override to customize headers, endpoint, or data if necessary."""
        return {}
