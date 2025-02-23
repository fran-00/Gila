from .api_client import APIClient


class ArliClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "ARLI"
        self.chat_history = []

    def _get_endpoint(self):
        return "https://api.arliai.com/v1/chat/completions"

    def _extract_response_data(self, response):
        ai_response = response["choices"][0]["message"]["content"]
        response_info = {
            "Prompt tokens": response.get("usage", {}).get("prompt_tokens", 0),
            "Completion tokens": response.get("usage", {}).get("completion_tokens", 0),
            "Total tokens": response.get("usage", {}).get("total_tokens", 0),
        }
        return ai_response, response_info
