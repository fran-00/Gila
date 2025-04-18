import requests

from ..api_client import APIClient


class DeepSeekClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "DEEPSEEK"

    def _get_endpoint(self):
        return "https://api.deepseek.com/chat/completions"

    def _send_request(self, endpoint, headers, data):
        """Override base method to show more specific errors"""
        try:
            response = requests.post(f"{endpoint}", headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            response_error = response.json()["error"]["message"]
            return {"error": str(response_error)}
