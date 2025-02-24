from .api_client import APIClient


class GoogleClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "GOOGLE"

    def _get_request_params(self):
        base_endpoint = self._get_endpoint()
        endpoint = f"{base_endpoint}/{self.llm}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [self.chat_history],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens,
            }
        }
        return {
            "headers": headers,
            "endpoint": endpoint,
            "data": data
        }

    def _get_endpoint(self):
        return "https://generativelanguage.googleapis.com/v1beta/models"

    def _format_user_message(self, prompt):
        return {"role": "user", "parts": [{"text": prompt}]}

    def _format_ai_message(self, ai_response):
        return {"role": "model", "parts": [{"text": ai_response}]}

    def _extract_response_data(self, response):
        ai_response = response["candidates"][0]["content"]["parts"][0]["text"]
        response_info = {
            "Prompt tokens": response.get("usageMetadata", {}).get("promptTokenCount", 0),
            "Completion tokens": response.get("usageMetadata", {}).get("candidatesTokenCount", 0),
            "Total tokens": response.get("usageMetadata", {}).get("totalTokenCount", 0),
        }
        return ai_response, response_info

    def validate_api_key(self, api_key):
        base_endpoint = self._get_endpoint()
        endpoint= f"{base_endpoint}/{self.llm}:generateContent?key={api_key}"
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "contents": [{
                "parts":[{"text": "test"}]
            }]
        }
        response = self._send_request(headers=headers, endpoint=endpoint, data=data)
        return False if "error" in response else True
