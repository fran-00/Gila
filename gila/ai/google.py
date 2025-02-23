from .api_client import APIClient


class GoogleClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "GOOGLE"
        self.chat_history = []

    def _get_endpoint(self):
        return "https://generativelanguage.googleapis.com/v1beta/models"

    def submit_prompt(self, prompt):
        self.chat_history.append({
            "role":"user",
            "parts":[{
                "text": prompt
            }]
        })
        base_endpoint = self._get_endpoint()
        endpoint= f"{base_endpoint}/{self.llm}:generateContent?key={self.api_key}"
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "contents": [self.chat_history],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens,
            }
        }
        try:
            response = self.send_request(headers=headers, endpoint=endpoint, data=data)
            ai_response, response_info = self._extract_response_data(response)
            self.chat_history.append({
                "role": "model",
                "parts":[{
                    "text": ai_response
                }]
            })
            return True, ai_response, response_info
        except KeyError as e:
            return False, str(e), None

    def _extract_response_data(self, response):
        ai_response = response["candidates"][0]["content"]["parts"][0]["text"]
        response_info = {
            "Prompt tokens": response.get("usageMetadata", {}).get("promptTokenCount", 0),
            "Completion tokens": response.get("usageMetadata", {}).get("candidatesTokenCount", 0),
            "Total tokens": response.get("usageMetadata", {}).get("totalTokenCount", 0),
        }
        return ai_response, response_info

    def on_chat_reset(self):
        self.chat_history = []
        self.chat_custom_name = None
        self.generate_chat_id()
