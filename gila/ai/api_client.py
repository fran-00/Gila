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
        self.system_message = None
        self.chat_history = []
        self.api_key = None
        self.chat_id = None
        self.chat_date = None
        self.chat_custom_name = None
        self.is_loaded = False
        self.last_response_info = None
        # For DALL-E 2 and 3
        self.image_size = None
        self.image_quality = None
        self.image_quantity = None

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

    def _send_request(self, endpoint, headers, data):
        try:
            response = requests.post(f"{endpoint}", headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def _get_request_params(self):
        """Override to customize headers, endpoint, or data if necessary."""
        endpoint = self._get_endpoint()
        headers = self._build_default_request_headers()
        data = self._build_default_request_data()
        return {
            "endpoint": endpoint,
            "headers": headers,
            "data": data,
        }

    def _build_default_request_headers(self):
        """Creates request headers with default values."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def _build_default_request_data(self):
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

    def _extract_response_data(self, response):
        """Extracts ai_response and response_info. Override if needed."""
        ai_response = response["choices"][0]["message"]["content"]
        response_info = {
            "Prompt tokens": response.get("usage", {}).get("prompt_tokens", 0),
            "Completion tokens": response.get("usage", {}).get("completion_tokens", 0),
            "Total tokens": response.get("usage", {}).get("total_tokens", 0),
        }
        return ai_response, response_info

    def validate_api_key(self, api_key):
        endpoint = self._get_endpoint()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": self.llm,
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": 5,
        }
        response = self._send_request(endpoint=endpoint, headers=headers, data=data)
        return False if "error" in response else True

    def submit_prompt(self, prompt):
        """Handles prompt submission."""
        self.chat_history.append(self._format_user_message(prompt))

        # Get request parameters (allows overrides for specific clients)
        params = self._get_request_params()

        try:
            response = self._send_request(**params)
            error_message = response.get("error")
            if error_message:
                raise Exception(error_message)

            ai_response, response_info = self._extract_response_data(response)
            self.last_response_info = response_info
            self.chat_history.append(self._format_ai_message(ai_response))

            return True, ai_response, response_info
        except Exception as e:
            return False, str(e), None

    def _format_user_message(self, prompt):
        """Defines how the user message should be formatted. Override if needed."""
        return {"role": "user", "content": prompt}

    def _format_ai_message(self, ai_response):
        """Defines how the AI response should be formatted. Override if needed."""
        return {"role": "assistant", "content": ai_response}

    def set_chat_history(self):
        """"""
        self.chat_history = self._set_system_message()

    def on_chat_reset(self):
        """This method is called by the controller whenever a chat is interrupted
        either by loading a saved one or starting a new one. In the first case,
        manager.restore_chat_from_id_slot will set it back to True """
        self.chat_history = self._set_system_message()
        self.chat_custom_name = None
        self.is_loaded = False
        self.generate_chat_id()

    def _set_system_message(self):
        """Include an optional message that sets the behavior and context for
        the AI assistant. Override if needed.
        """
        return [{"role": "system", "content": self.system_message}] if self.system_message else []
