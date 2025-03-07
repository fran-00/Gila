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
        # For o-series models
        self.reasoning_effort = None

    def check_if_api_key(self, company_name):
        """Check for the presence of an API key in the .env file for the
        specified company.

        Loads the environment variables from the .env file and retrieves the API
        key associated with the given company name. If an API key is found, it
        assigns the key to the instance variable and returns a boolean value.

        Parameters:
            company_name (str): The name of the company for which to check the API key.

        Returns:
            bool: True if an API key is found and retrieved, False otherwise.
        """
        load_dotenv()
        if key := os.getenv(f"{company_name}_API_KEY"):
            self.api_key = key
            return True
        return False

    def get_api_key(self):
        """Return API Key"""
        return self.api_key

    def get_chat_history(self):
        """Return chat history"""
        return self.chat_history

    def generate_chat_id(self):
        """Generate a unique chat ID consisting of random alphanumeric characters.

        Creates a chat ID by randomly selecting 10 characters from the set of
        ASCII letters and digits. The generated ID is assigned to the instance's
        chat_id.
        """
        self.chat_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    def _send_request(self, endpoint, headers, data):
        """Send a POST request to the specified endpoint with the given headers
        and data.

        Constructs and sends a POST request to the provided endpoint and includes
        the specified headers and data in JSON format.
        If the request is successful, it returns the JSON response. If an error
        occurs during the request, it catches the exception and returns a
        dictionary containing the error message.

        Parameters:
            endpoint (str): The URL of the endpoint to send the request to.
            headers (dict): A dictionary of HTTP headers to include in the request.
            data (dict): The data to be sent in the body of the request,
                         serialized as JSON.

        Returns:
            dict: The JSON response from the server or an error message.
        """
        try:
            response = requests.post(f"{endpoint}", headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def _get_request_params(self):
        """Retrieve the parameters for a request, including the endpoint,
        headers, and data.

        This can be overridden to customize the HTTP request parameters as needed.
        By default, it constructs the endpoint, headers, and data using helper
        methods and returns them in a dictionary.

        Returns:
            dict: A dictionary containing the request parameters with the keys:
                - endpoint (str): The URL of the endpoint for the request.
                - headers (dict): A dictionary of HTTP headers for the request.
                - data (dict): The data to be sent in the body of the request.
        """
        endpoint = self._get_endpoint()
        headers = self._build_default_request_headers()
        data = self._build_default_request_data()
        return {
            "endpoint": endpoint,
            "headers": headers,
            "data": data,
        }

    def _build_default_request_headers(self):
        """Create and return the default request headers.

        Constructs a dictionary of HTTP headers to be used in requests. 
        By default, it includes the content type as "application/json" and an
        authorization header that contains the API key.

        Returns:
            dict: A dictionary containing the default request headers with the keys:
                - content-type (str): The media type of the resource, set to "application/json".
                - authorization (str): The authorization token in the format "bearer {api_key}".
        """
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def _build_default_request_data(self):
        """Create and return the default request data.

        Constructs a dictionary of data to be sent in the body of the request.
        By default, it includes the model name, chat history, temperature, and
        maximum tokens.

        Returns:
            dict: A dictionary containing the default request data with the keys:
                - model (str): The name of the language model being used.
                - messages (list): The history of messages in the chat.
                - temperature (float): The sampling temperature for the model.
                - max_tokens (int): The maximum number of tokens to generate in
                                    the response.
        """
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
        """Extract the AI response and response information from the API response.

        Retrieves the AI-generated response content and relevant usage information
        from the provided response dictionary. It extracts the response content
        from the first choice and gathers token usage statistics.
        This method can be overridden to customize the extraction process if needed.

        Parameters:
            response (dict): The response dictionary returned from the API.

        Returns:
            tuple: A tuple containing:
                - ai_response (str): The content of the AI response.
                - response_info (dict): A dictionary with token usage information, including:
                    - prompt tokens (int): The number of tokens used in the prompt.
                    - completion tokens (int): The number of tokens generated in the completion.
                    - total tokens (int): The total number of tokens used in the request.
        """
        ai_response = response["choices"][0]["message"]["content"]
        response_info = {
            "Prompt tokens": response.get("usage", {}).get("prompt_tokens", 0),
            "Completion tokens": response.get("usage", {}).get("completion_tokens", 0),
            "Total tokens": response.get("usage", {}).get("total_tokens", 0),
        }
        return ai_response, response_info

    def validate_api_key(self, api_key):
        """Validate the provided API key by sending a test request.

        Constructs a request with the given API key to check if it is valid.
        It sends a test message to the API and evaluates the response: if the
        response contains an error, the method returns False.

        Parameters:
            api_key (str): The API key to validate.

        Returns:
            bool: True if the API key is valid, False otherwise.
        """
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
        """Handle the submission of a user prompt to the AI model.

        Appends the formatted user message to the chat history, retrieves the
        request parameters, and sends the request to the API. If the response
        contains an error, it raises an exception. If the request is successful,
        extracts the AI response and updates the chat history with the AI's message.

        Parameters:
            prompt (str): The user's prompt to be submitted to the AI.

        Returns:
            tuple: A tuple containing:
                - success (bool): True if the prompt submission was successful,
                                  False otherwise.
                - ai_response (str or None): The AI's response if successful,
                                             or None if failed.
                - response_info (dict or None): Information about the response
                                                if successful, or None if failed.
        """
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
        """Define how the user message should be formatted for API submission.

        Formats the user's prompt into a dictionary with the appropriate structure
        for the API request. This method can be overridden to customize the
        formatting as needed.

        Parameters:
            prompt (str): The user's message to be formatted.

        Returns:
            dict: A dictionary representing the formatted user message with keys:
                - role (str): The role of the message sender, set to "user".
                - content (str): The content of the user's message.
        """
        return {"role": "user", "content": prompt}

    def _format_ai_message(self, ai_response):
        """Define how the AI response should be formatted for API submission.

        Formats the AI's response into a dictionary with the appropriate
        structure for the API request. This method can be overridden to customize
        the formatting as needed.

        Parameters:
            ai_response (str): The AI's response to be formatted.

        Returns:
            dict: A dictionary representing the formatted AI message with keys:
                - role (str): The role of the message sender, set to "assistant".
                - content (str): The content of the AI's response.
        """
        return {"role": "assistant", "content": ai_response}

    def set_chat_history(self):
        """Initialize the chat history with the system message.

        Sets the chat history to the output of the _set_system_message method,
        which includes the system message that defines the behavior and context
        for the AI assistant.
        """
        self.chat_history = self._set_system_message()

    def on_chat_reset(self):
        """Reset the chat state when a chat is interrupted.

        Called by the controller whenever a chat is interrupted, either by
        loading a saved chat or starting a new one. In the case of loading, 
        the manager's restore_chat_from_id_slot will set the loaded state to True. 
        Initializes the chat history with the system message, clears the custom
        chat name, sets the loaded state to False, and generates a new chat ID.
        """
        self.chat_history = self._set_system_message()
        self.chat_custom_name = None
        self.is_loaded = False
        self.generate_chat_id()

    def _set_system_message(self):
        """Include an optional message that sets the behavior and context for
        the AI assistant.

        Returns a list containing a system message formatted for the API.
        If a system message is defined, it includes the role as "system" and
        the content as the system message. If no system message is set, it
        returns an empty list. This method can be overridden to customize the
        system message as needed.

        Returns:
            list: A list containing the system message formatted as a dictionary,
            or an empty list if no message is set.
        """
        return [{"role": "system", "content": self.system_message}] if self.system_message else []
