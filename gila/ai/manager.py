import os
import json
import pickle
import requests
import sys
from datetime import datetime

from PySide6.QtCore import QObject, Slot, Signal

from .clients import (
    AnthropicClient,
    ArliClient,
    CohereClient,
    DeepSeekClient,
    GoogleClient,
    GroqClient,
    MistralClient,
    GPTClient,
    OClient,
    DALLEClient
)


CLASS_MAP = {
    "GPTClient": GPTClient,
    "OClient": OClient,
    "GoogleClient": GoogleClient,
    "GroqClient": GroqClient,
    "AnthropicClient": AnthropicClient,
    "ArliClient": ArliClient,
    "CohereClient": CohereClient,
    "DeepSeekClient": DeepSeekClient,
    "MistralClient": MistralClient,
    "DALLEClient": DALLEClient
}

COMPANIES = {
    "ANTHROPIC": AnthropicClient("claude-3-5-sonnet-latest"),
    "ARLI": ArliClient("Llama-3.3-70B-Instruct"),
    "COHERE": CohereClient("command"),
    "DEEPSEEK": DeepSeekClient("deepseek-chat"),
    "GOOGLE": GoogleClient("gemini-2.0-flash"),
    "GROQ": GroqClient("gemma2-9b-it"),
    "MISTRAL": MistralClient("mistral-small-latest"),
    "OPENAI": GPTClient("gpt-4o-mini"),
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
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    relative_path = "storage/models.json"
    file_path = os.path.join(base_path, relative_path)

    with open(file_path, 'r') as file:
        models_data = json.load(file)

    available_models = {}
    for model_name, data in models_data.items():
        if client_data := data.get("client"):
            class_name = client_data.get("class")
            params = client_data.get("model", [])
            if client_class := CLASS_MAP.get(class_name):
                available_models[model_name] = client_class(*params)
            else:
                print(f"Class {class_name} not found for {model_name}.")
        else:
            print(f"Data not found for model {model_name}.")
    return available_models


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
        self.next_reasoning_effort = None
        self.get_saved_settings()

    def get_saved_settings(self):
        """Load saved settings from a JSON file, creating default settings if
        the file does not exist.

        Checks for the existence of the settings file. If the file is not found,
        creates the file with default settings. Then reads the settings from the
        file, initializes the client with the loaded parameters, and generates a
        chat ID for the client.

        Attributes set on the client include:
            - llm_name: The name of the language model.
            - temperature: The sampling temperature for the model.
            - max_tokens: The maximum number of tokens to generate.
            - system_message: The system message to guide the assistant's behavior.
            - image_size: The desired size for generated images.
            - image_quality: The quality setting for generated images.
            - image_quantity: The number of images to generate.
            - reasoning_effort: How many reasoning tokens model should generate

        Raises:
            FileNotFoundError: If the settings file cannot be created.
            json.JSONDecodeError: If the settings file is not a valid JSON.
        """
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
                "reasoning_effort": "medium"
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
            self.client.reasoning_effort = data.get("reasoning_effort")

        self.client.generate_chat_id()

    def update_saved_settings(self):
        """Update the saved settings in the JSON file with the current client
        parameters.

        Reads the existing settings from file, updates the settings with current
        values from the client attributes and then writes the updated settings
        back to the file. 

        Attributes updated include:
            - llm_name: The name of the language model.
            - temperature: The sampling temperature for the model.
            - max_tokens: The maximum number of tokens to generate.
            - system_message: The system message to guide the assistant's behavior.
            - image_size: The desired size for generated images.
            - image_quality: The quality setting for generated images.
            - image_quantity: The number of images to generate.
            - reasoning_effort: How many reasoning tokens model should generate

        Raises:
            FileNotFoundError: If the settings file does not exist.
            json.JSONDecodeError: If the settings file is not a valid JSON.
        """
        with open("storage/saved_settings.json", "r") as f:
            data = json.load(f)
            data["llm_name"] = self.client.llm_name
            data["temperature"] = self.client.temperature
            data["max_tokens"] = self.client.max_tokens
            data["system_message"] = self.client.system_message
            data["image_size"] = self.client.image_size
            data["image_quality"] = self.client.image_quality
            data["image_quantity"] = self.client.image_quantity
            data["reasoning_effort"] = self.client.reasoning_effort

        with open("storage/saved_settings.json", "w") as file:
            json.dump(data, file, indent=4)

    def on_api_key(self):
        """Check if the API key for the specified company is present in the
        storage/api_keys.json file.

        Called by the controller's chat_started_slot. Asks the client to verify
        the presence of the API key for the current company. If the API key is
        found, it retrieves the key and returns True; otherwise, it returns False.

        Returns:
            bool: True if the API key is present and retrieved, False otherwise.
        """
        if self.client.check_if_api_key(self.client.company) is True:
            self.client.get_api_key()
            return True
        return False

    @Slot(str, float, int, str, str, str, int, str)
    def set_new_settings_slot(
        self,
        new_llm,
        new_temperature,
        new_max_tokens,
        new_system_message,
        new_image_size,
        new_image_quality,
        new_image_quantity,
        new_reasoning_effort
    ):
        """Slot 
        Connected to one signal:
        - controller.new_settings_to_manager

        When triggered, takes new settings for the language model and updates
        the client configuration accordingly. It sets the new language model,
        adjusts the temperature, and updates other parameters related to the
        client's settings. next_client is a tuple containing the selected client
        instance and its name, which is utilized in the controller.chat_started_slot
        method.

        Parameters:
            new_llm (str): The name of the new language model to be used.
            new_temperature (float): The new sampling temperature for the model.
            new_max_tokens (int): The new maximum number of tokens to generate.
            new_system_message (str): The new system message for guiding the assistant's behavior.
            new_image_size (str): The new desired size for generated images.
            new_image_quality (str): The new quality setting for generated images.
            new_image_quantity (int): The new number of images to generate.
            new_reasoning_effort (str): The new amount of reasoning tokens to generate.
        """
        selected_llm = AVAILABLE_MODELS.get(new_llm)
        self.next_client = selected_llm, new_llm
        self.next_temperature = new_temperature / 10
        self.next_max_tokens = new_max_tokens
        self.next_system_message = new_system_message
        self.next_image_size = new_image_size
        self.next_image_quality = new_image_quality
        self.next_image_quantity = new_image_quantity
        self.next_reasoning_effort = new_reasoning_effort

    @Slot(str)
    def api_key_slot(self, api_key, company_name):
        """Slot
        Connected to one signal:
        - controller.api_key_to_manager

        When triggered, checks the validity of the provided API key. If 
        company_name is None, it sends the new API key to the current client; 
        otherwise, it sends it to the client associated with the specified
        company name. Then emits a boolean signal indicating whether the API
        key is valid. If the key is valid, it calls the save_api_key method to
        store it. If the company_name is not found, defaults to using the
        currently selected client.

        Parameters:
            api_key (str): The API key to validate.
            company_name (str): The name of the company associated with the API key.
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

        When triggered, reads saved chat settings from a file and applies them
        to the client. It loads the chat data associated with the provided
        chat_id from a pickle file, updates the client's attributes with the
        loaded data, and prepares the client for use with the restored chat.
        The method retrieves the client based on the language model name
        stored in the chat data.

        Parameters:
            chat_id (str): The unique identifier for the chat to restore.
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
        self.client.reasoning_effort = chat["reasoning_effort"]

    def on_current_settings(self):
        """Return the current settings of the client.

        Retrieves and returns a tuple containing various attributes of the
        current client.

        Returns:
            tuple: A tuple containing the current client's settings:
                - chat_id (str): The unique identifier for the chat.
                - chat_custom_name (str): The custom name for the chat.
                - llm_name (str): The name of the language model being used.
                - temperature (float): The temperature for the model.
                - max_tokens (int): The maximum number of tokens to generate.
                - chat_date (str): The date of the chat.
                - system_message (str): The system message guiding ai behavior.
                - image_size (str): The size of generated images.
                - image_quality (str): The quality setting for generated images.
                - image_quantity (int): The number of images to generate.
                - reasoning_effort (str): The amount of reasoning tokens generate.
        """
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
            self.client.reasoning_effort,
        )

    def save_api_key(self, api_key, company_name):
        """Save the validated API key to the .env file.

        Appends the API key for the specified company name to the .env file
        without overwriting existing data in the format:
        COMPANY_NAME_api_key='API_KEY'.
        The company name is converted to uppercase.

        Parameters:
            api_key (str): The validated API key to be saved.
            company_name (str): The name of the company associated with the API key.
        """
        with open(".env", "a") as file:
            file.write(f"\n{company_name.upper()}_API_KEY='{api_key}'")

    def check_internet_connection(self):
        """Check the availability of an internet connection.

        Attempts to send a HEAD request to "http://www.google.com/" to verify
        if a connection can be established. If the request is successful, it
        returns True; otherwise, it catches a connection error and returns False.

        Returns:
            bool: True if the internet connection is available, False otherwise.
        """
        try:
            requests.head("http://www.google.com/", timeout=3)
            return True
        except requests.ConnectionError:
            return False

    def save_current_chat(self):
        """Save the current chat's settings and history to a pickle file.

        Creates a dictionary containing the current chat's attributes. The data
        is serialized and saved to a file named with the chat ID in the
        "storage/saved_data" directory. The chat date is formatted as 
        "day-month-year hour:minute:second".
        """
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
                "reasoning_effort": self.client.reasoning_effort,
            }
        }
        with open(f"storage/saved_data/{self.client.chat_id}.pk", "wb") as file:
            pickle.dump(data, file)
