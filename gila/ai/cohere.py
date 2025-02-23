import cohere

from .api_client import APIClient


class CohereClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "COHERE"
        self.chat_history = []

    def submit_api_key(self):
        self.co = cohere.Client(self.get_api_key())

    def submit_prompt(self, prompt):
        self.chat_history.append({"role": "user", "content": prompt})
        endpoint = "https://api.cohere.com/v2/chat"
        data = {
            "model": self.llm,
            "messages": self.chat_history,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        try:
            response = self.send_request(endpoint, data)
            response_info = {
                "Prompt tokens": response.get("usage", {}).get("tokens", {}).get("input_tokens", 0),
                "Completion tokens": response.get("usage", {}).get("tokens", {}).get("output_tokens", 0),
                "Total tokens": None
            }
            ai_response = response["message"]["content"][0]["text"]
            self.chat_history.append({"role": "assistant", "content": ai_response})

            return True, ai_response, response_info
        except KeyError as e:
            return False, str(e), None

    def on_chat_reset(self):
        self.chat_history = []
        self.chat_custom_name = None
        self.generate_chat_id()

    def validate_api_key(self, api_key):
        test_co = cohere.Client(api_key)
        try:
            test_co.generate(prompt='test')
            return True
        except cohere.errors.unauthorized_error.UnauthorizedError as e:
            return False
