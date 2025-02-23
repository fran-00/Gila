from .api_client import APIClient


class OpenAIClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "OPENAI"
        self.chat_history = [{"role": "system", "content": "You are an helpful assistant."}]

    def _get_endpoint(self):
        return "https://api.openai.com/v1/chat/completions"

    def _extract_response_data(self, response):
        ai_response = response["choices"][0]["message"]["content"]
        response_info = {
            "Prompt tokens": response.get("usage", {}).get("prompt_tokens", 0),
            "Completion tokens": response.get("usage", {}).get("completion_tokens", 0),
            "Total tokens": response.get("usage", {}).get("total_tokens", 0),
        }
        return ai_response, response_info

    def on_image_generations(self, prompt):
        endpoint = "https://api.openai.com/v1/images/generations"
        data = {
            "model": self.llm,
            "prompt": prompt,
            "n": 1,
            "size": "256x256"
        }
        try:
            response = self._send_request(endpoint, data)
            image_url = response["data"][0]["url"]
            return True, image_url, None
        except KeyError as e:
            return False, str(e), None

    def on_chat_reset(self):
        self.chat_history = [{"role": "system", "content": "You are an helpful assistant."}]
        self.chat_custom_name = None
        self.generate_chat_id()
