import os
import json
import pickle
import requests
from datetime import datetime

from PySide6.QtCore import QObject, Slot, Signal

from .clients import (
    AnthropicClient,
    ArliClient,
    CohereClient,
    DeepSeekClient,
    GoogleClient,
    MistralClient,
    OpenAIClient,
    OpenAIDalleClient
)


CLASS_MAP = {
    "OpenAIClient": OpenAIClient,
    "GoogleClient": GoogleClient,
    "AnthropicClient": AnthropicClient,
    "ArliClient": ArliClient,
    "CohereClient": CohereClient,
    "DeepSeekClient": DeepSeekClient,
    "MistralClient": MistralClient,
    "OpenAIDalleClient": OpenAIDalleClient
}

COMPANIES = {
    "ANTHROPIC": AnthropicClient("claude-3-sonnet-20240229"),
    "ARLI": ArliClient("Llama-3.3-70B-Instruct"),
    "COHERE": CohereClient("command"),
    "DEEPSEEK": DeepSeekClient("deepseek-chat"),
    "GOOGLE": GoogleClient("gemini-2.0-flash"),
    "MISTRAL": MistralClient("mistral-small-latest"),
    "OPENAI": OpenAIClient("gpt-4o-mini"),
}

def load_available_models_from_json():
    """Load model data from the JSON file and recreate client instances.

    The JSON file must have the following structure for each model:

        {
            "Readable Model Name": {
                "limits": [max_tokens, max_temperature],
                "client": {
                    "class": "ClassName",
                    "model": ["model-name"]
                }
            },
            ...
        }

    Returns:
        dict: A dictionary where the keys are the model names and the values
        are the corresponding client instances. If the JSON file is not found,
        an empty dictionary is returned.
    """
    try:
        with open('storage/models.json', 'r') as file:
            models_data = json.load(file)

        available_models = {}
        for model_name, data in models_data.items():
            client_data = data.get("client")
            if client_data:
                class_name = client_data.get("class")
                params = client_data.get("model", [])
                client_class = CLASS_MAP.get(class_name)
                if client_class:
                    available_models[model_name] = client_class(*params)
                else:
                    print(f"Class {class_name} not found for {model_name}.")
            else:
                print(f"Data not found for model {model_name}.")
        return available_models

    except FileNotFoundError:
        print("File models.json not found.")
        return {}

AVAILABLE_MODELS = load_available_models_from_json()


class AIManager(QObject):
    api_key_is_valid_to_controller = Signal(bool)

    def __init__(self):
        super().__init__()
        self.client = None
        self.stream_stopped = True
        self.next_client = None
        self.next_temperature = None
        self.next_max_tokens = None
        self.next_system_message = None
        self.next_image_size = None
        self.next_image_quality = None
        self.next_image_quantity = None
        self.get_saved_settings()

    def get_saved_settings(self):
        file_path = "storage/saved_settings.json"
        if not os.path.exists(file_path):
            default_data = {
                "llm_name": "GPT-4o mini",
                "temperature": 1.0,
                "max_tokens": 4096,
                "system_message": "You are an helpful assistant.",
                "image_size": "1024x1024",
                "image_quality": "standard",
                "image_quantity": 1,
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
            self.client.system_message = data.get("system_message")
            self.client.image_size = data.get("image_size")
            self.client.image_quality = data.get("image_quality")
            self.client.image_quantity = data.get("image_quantity")

        self.client.generate_chat_id()

    def update_saved_settings(self):
        with open("storage/saved_settings.json", "r") as f:
            data = json.load(f)
            data["llm_name"] = self.client.llm_name
            data["temperature"] = self.client.temperature
            data["max_tokens"] = self.client.max_tokens
            data["system_message"] = self.client.system_message
            data["image_size"] = self.client.image_size
            data["image_quality"] = self.client.image_quality
            data["image_quantity"] = self.client.image_quantity

        with open("storage/saved_settings.json", "w") as file:
            json.dump(data, file, indent=4)

    def on_api_key(self):
        """Called by Controller's chat_started_slot, asks client to check if
        API key of the said company is present on the storage/api_keys.json file.
        Returns a boolean with response"""
        if self.client.check_if_api_key(self.client.company) is True:
            self.client.get_api_key()
            return True
        return False

    @Slot(str, float, int, str, str, str, int)
    def set_new_settings_slot(
        self,
        new_llm,
        new_temperature,
        new_max_tokens,
        new_system_message,
        new_image_size,
        new_image_quality,
        new_image_quantity
    ):
        """Slot
        Connected to one signal:
            - controller.new_settings_to_manager
        When triggered, takes new llm name and sets new client on call

        next_client is a tuple because the first element is the class instance,
        while the second element is the name of the selected client: you can see
        the reason for this in controller.chat_started_slot method
        """
        selected_llm = AVAILABLE_MODELS.get(new_llm)
        self.next_client = selected_llm, new_llm
        self.next_temperature = new_temperature / 10
        self.next_max_tokens = new_max_tokens
        self.next_system_message = new_system_message
        self.next_image_size = new_image_size
        self.next_image_quality = new_image_quality
        self.next_image_quantity = new_image_quantity

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
        self.client.is_loaded = True
        self.client.chat_custom_name = chat["chat_custom_name"]
        self.client.llm_name = chat["llm_name"]
        self.client.temperature = chat["temperature"]
        self.client.max_tokens = chat["max_tokens"]
        self.client.chat_history = chat["chat_history"]
        self.client.chat_date = chat["chat_date"]
        self.client.system_message = chat["system_message"]
        self.client.last_response_info = chat["last_response_info"]
        self.client.image_size = chat["image_size"]
        self.client.image_quality = chat["image_quality"]
        self.client.image_quantity = chat["image_quantity"]

    def on_current_settings(self):
        """Return current client's settings"""
        return (
            self.client.chat_id,
            self.client.chat_custom_name,
            self.client.llm_name,
            self.client.temperature,
            self.client.max_tokens,
            self.client.chat_date,
            self.client.system_message,
            self.client.image_size,
            self.client.image_quality,
            self.client.image_quantity,
        )

    def save_api_key(self, api_key, company_name):
        """Saves validated API Key to api_keys.json file"""
        with open(".env", "a") as file:
            file.write(f"\n{company_name.upper()}_API_KEY='{api_key}'")

    def check_internet_connection(self):
        try:
            requests.head("http://www.google.com/", timeout=3)
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
                "system_message": self.client.system_message,
                "last_response_info": self.client.last_response_info,
                "image_size": self.client.image_size,
                "image_quality": self.client.image_quality,
                "image_quantity": self.client.image_quantity,
            }
        }
        with open(f"storage/saved_data/{self.client.chat_id}.pk", "wb") as file:
            pickle.dump(data, file)
