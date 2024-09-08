import os
import json
import pickle
import requests
from datetime import datetime

from PySide6.QtCore import QObject, Slot, Signal

from .openai import OpenAIClient
from .google import GoogleClient
from .cohere import CohereClient
from .mistral import MistralClient
from .anthropic import AnthropicClient


AVAILABLE_MODELS = {
    "Claude 3 Haiku": AnthropicClient("claude-3-haiku-20240307"),
    "Claude 3 Opus": AnthropicClient("claude-3-opus-20240229"),
    "Claude 3 Sonnet": AnthropicClient("claude-3-sonnet-20240229"),
    "Claude 3.5 Sonnet": AnthropicClient("claude-3-5-sonnet-20240620"),
    "Command": CohereClient("command"),
    "Command R": CohereClient("command-r"),
    "Command R+": CohereClient("command-r-plus"),
    "DALL-E-2": OpenAIClient("dall-e-2"),
    "DALL-E-3": OpenAIClient("dall-e-3"),
    "Gemini 1.5 Flash": GoogleClient("gemini-1.5-flash"),
    "Gemini 1.5 Pro": GoogleClient("gemini-1.5-pro"),
    "Gemini 1.0 Pro": GoogleClient("gemini-1.0-pro"),
    "GPT-4": OpenAIClient("gpt-4"),
    "GPT-4 Turbo": OpenAIClient("gpt-4-turbo"),
    "GPT-4o": OpenAIClient("gpt-4o"),
    "GPT-4o mini": OpenAIClient("gpt-4o-mini"),
    "Mistral Large": MistralClient("mistral-large-latest"),
    "Mistral Nemo": MistralClient("open-mistral-nemo"),
}

COMPANIES = {
    "ANTHROPIC": AnthropicClient("claude-3-sonnet-20240229"),
    "COHERE": CohereClient("command"),
    "GOOGLE": GoogleClient("gemini-1.5-flash"),
    "MISTRAL": CohereClient("mistral-large-latest"),
    "OPENAI": OpenAIClient("gpt-4o-mini"),
}


class AIManager(QObject):
    api_key_is_valid_to_controller = Signal(bool)

    def __init__(self):
        super().__init__()
        self.client = None
        self.stream_stopped = True
        self.next_client = None
        self.next_temperature = None
        self.next_max_tokens = None
        self.get_saved_settings()

    def get_saved_settings(self):
        file_path = "storage/saved_settings.json"
        if not os.path.exists(file_path):
            default_data = {
                "llm_name": "GPT-4o mini",
                "temperature": 1.0,
                "max_tokens": 4096,
            }
            with open(file_path, "w") as f:
                json.dump(default_data, f)

        with open(file_path, "r") as f:
            data = json.load(f)
            llm_name = data.get("llm_name")
            self.client = AVAILABLE_MODELS.get(llm_name)
            self.client.llm_name = llm_name
            self.client.temperature = data.get("temperature")
            self.client.max_tokens = data.get("max_tokens")
        self.client.generate_chat_id()

    def update_saved_settings(self):
        with open("storage/saved_settings.json", "r") as f:
            data = json.load(f)
            data["llm_name"] = self.client.llm_name
            data["temperature"] = self.client.temperature
            data["max_tokens"] = self.client.max_tokens

        with open("storage/saved_settings.json", "w") as file:
            json.dump(data, file, indent=4)

    def on_api_key(self):
        """Called by Controller's new_chat_started_slot, asks client to check if
        API key of the said company is present on the storage/api_keys.json file.
        Returns a boolean with response"""
        if self.client.check_if_api_key(self.client.company) is True:
            self.client.submit_api_key()
            return True
        return False

    @Slot(str, float, int)
    def set_new_settings_slot(self, new_llm, new_temperature, new_max_tokens):
        """Slot
        Connected to one signal:
            - controller.selected_client_to_manager
        When triggered, takes new llm name and sets new client on call

        next_client is a tuple because the first element is the class instance,
        while the second element is the name of the selected client: you can see
        the reason for this in controller.new_chat_started_slot method
        """
        selected_llm = AVAILABLE_MODELS.get(new_llm)
        self.next_client = selected_llm, new_llm
        self.next_temperature = new_temperature / 10
        self.next_max_tokens = new_max_tokens

    @Slot(str)
    def api_key_slot(self, api_key, company_name):
        """Slot
        Connected to one signal:
            - controller.api_key_to_manager
        When triggered, if company_name is None, manager will send new API key
        to the current client, else it will send it on the client based on that
        company name. API key is then sent to client to check if is valid and
        emits a boolean signal with response. If key is valid, calls save_api_key
        """
        client = COMPANIES.get(company_name.upper())
        if client is None:
            client = AVAILABLE_MODELS.get(self.client.llm_name)
        validated = client.validate_api_key(api_key)
        if validated is True:
            self.api_key_is_valid_to_controller.emit(True)
            self.save_api_key(api_key, company_name)
        else:
            self.api_key_is_valid_to_controller.emit(False)

    @Slot(str)
    def restore_chat_from_id_slot(self, chat_id):
        """Slot
        Connected to one signal:
            - controller.loading_saved_chat_id_to_manager
        Reads saved chats settings from file and applies them to client
        """
        with open(f"storage/saved_data/{chat_id}.pk", "rb") as file:
            saved_data = pickle.load(file)
            chat = saved_data[chat_id]
        # Due to pickle limitation we have to get the client from its name
        self.client = AVAILABLE_MODELS.get(chat["llm_name"])
        self.client.chat_id = chat_id
        self.client.chat_custom_name = chat["chat_custom_name"]
        self.client.llm_name = chat["llm_name"]
        self.client.temperature = chat["temperature"]
        self.client.max_tokens = chat["max_tokens"]
        self.client.chat_history = chat["chat_history"]
        self.client.chat_date = chat["chat_date"]

    def on_current_settings(self):
        """Return current client's settings"""
        return (
            self.client.chat_id,
            self.client.chat_custom_name,
            self.client.llm_name,
            self.client.temperature,
            self.client.max_tokens,
            self.client.chat_date,
        )

    def save_api_key(self, api_key, company_name):
        """Saves validated API Key to api_keys.json file"""
        with open(".env", "a") as file:
            file.write(f"\n{company_name.upper()}_API_KEY='{api_key}'")

    def check_internet_connection(self):
        try:
            requests.head("http://www.google.com/", timeout=1)
            return True
        except requests.ConnectionError:
            return False

    def save_current_chat(self):
        date = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        data = {
            self.client.chat_id: {
                "chat_custom_name": self.client.chat_custom_name,
                "llm_name": self.client.llm_name,
                "temperature": self.client.temperature,
                "max_tokens": self.client.max_tokens,
                "chat_date": date,
                "chat_history": self.client.chat_history,
                "chat_log": None,
            }
        }
        with open(f"storage/saved_data/{self.client.chat_id}.pk", "wb") as file:
            pickle.dump(data, file)
