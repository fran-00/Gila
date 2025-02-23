from .api_client import APIClient


class AnthropicClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "ANTHROPIC"
        self.chat_history = []

    def _get_endpoint(self):
        return "https://api.anthropic.com/v1/messages"

    def _get_request_params(self):
        endpoint = self._get_endpoint()
        headers = {
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": f"{self.api_key}"
        }
        data = self._build_default_request_data()
        return {
            "endpoint": endpoint,
            "headers": headers,
            "data": data,
        }

    def _extract_response_data(self, response):
        ai_response = response["content"][0]["text"]
        response_info = {
            "Prompt tokens": response.get("usage", {}).get("tokens", {}).get("input_tokens", 0),
            "Completion tokens": response.get("usage", {}).get("tokens", {}).get("output_tokens", 0),
            "Total tokens": None
        }
        return ai_response, response_info
