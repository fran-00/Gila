from .api_client import APIClient


class AnthropicClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "ANTHROPIC"
        self.chat_history = []

    def _get_endpoint(self):
        return "https://api.anthropic.com/v1/messages"

    def submit_prompt(self, prompt):
        self.chat_history.append({"role": "user", "content": prompt})
        headers = {
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": f"{self.api_key}"
        }
        try:
            response = self.send_request(headers=headers)
            ai_response, response_info = self._extract_response_data(response)
            self.chat_history.append({"role": "assistant", "content": ai_response})
            return True, ai_response, response_info
        except KeyError as e:
            return False, str(e), None

    def _extract_response_data(self, response):
        ai_response = response["content"][0]["text"]
        response_info = {
            "Prompt tokens": response.get("usage", {}).get("tokens", {}).get("input_tokens", 0),
            "Completion tokens": response.get("usage", {}).get("tokens", {}).get("output_tokens", 0),
            "Total tokens": None
        }
        return ai_response, response_info

    def on_chat_reset(self):
        self.chat_history = []
        self.chat_custom_name = None
        self.generate_chat_id()
