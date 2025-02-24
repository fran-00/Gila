from .api_client import APIClient


class OpenAIClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "OPENAI"
        self.chat_history = [{"role": "system", "content": "You are an helpful assistant."}]

    def _get_endpoint(self):
        return "https://api.openai.com/v1/chat/completions"


class OpenAIDalleClient(APIClient):
    def __init__(self, llm):
        super().__init__(llm)
        self.company = "OPENAI"

    def _get_endpoint(self):
        return "https://api.openai.com/v1/images/generations"

    def _get_request_params(self, prompt):
        endpoint = self._get_endpoint()
        headers = self._build_default_request_headers()
        data = {
            "model": self.llm,
            "prompt": prompt,
            "n": 1,
            "size": "256x256"
        }
        return {
            "endpoint": endpoint,
            "headers": headers,
            "data": data,
        }
    
    def submit_prompt(self, prompt):
        params = self._get_request_params(prompt)
        try:
            response = self._send_request(**params)
            print(response)
            ai_response, response_info = self._extract_response_data(response)

            return True, ai_response, response_info
        except KeyError as e:
            return False, str(e), None

    def _extract_response_data(self, response):
        ai_response = response["data"][0]["url"]
        response_info = {
            "Prompt tokens": None,
            "Completion tokens": None,
            "Total tokens": None
        }
        return ai_response, response_info
