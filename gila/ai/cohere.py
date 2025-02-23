import cohere

from .api_client import APIClient


class CohereClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "COHERE"
        self.chat_history = []

    def _get_endpoint(self):
        return "https://api.cohere.com/v2/chat"

    def submit_prompt(self, prompt):
        self.chat_history.append({"role": "user", "content": prompt})
        try:
            response = self.send_request()
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
