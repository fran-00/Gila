from ..api_client import APIClient


class OpenAIClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "OPENAI"

    def _get_endpoint(self):
        return "https://api.openai.com/v1/chat/completions"


class GPTClient(OpenAIClient):

    def __init__(self, llm):
        super().__init__(llm)

    def _set_system_message(self):
        """Required role for system message is <developer>"""
        return [{"role": "developer", "content": self.system_message}] if self.system_message else []


class OClient(OpenAIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.max_completion_tokens = self.max_tokens

    def _build_default_request_data(self):
        """Max tokens and temperature are not supported with o-series models"""
        return {
            "model": self.llm,
            "reasoning_effort": self.reasoning_effort.lower(),
            "messages": self.chat_history,
            "max_completion_tokens": self.max_completion_tokens
        }

    def _set_system_message(self):
        """o1-mini model currently doesn't support developer message"""
        if self.llm not in ["o1-mini"]:
            return [{"role": "developer", "content": self.system_message}] if self.system_message else []
        else:
            return []


class DALLEClient(OpenAIClient):
    def __init__(self, llm):
        super().__init__(llm)

    def _get_endpoint(self):
        return "https://api.openai.com/v1/images/generations"

    def _get_request_params(self, prompt):
        endpoint = self._get_endpoint()
        headers = self._build_default_request_headers()
        data = {
            "model": self.llm,
            "prompt": prompt,
            "size": self.image_size,
        }
        if self.llm in ["dall-e-2"]:
            data['n'] = self.image_quantity
            data['quality'] = self.image_quality.lower()
        return {
            "endpoint": endpoint,
            "headers": headers,
            "data": data,
        }
    
    def submit_prompt(self, prompt):
        params = self._get_request_params(prompt)
        try:
            response = self._send_request(**params)
            error_message = response.get("error")
            if error_message:
                raise Exception(error_message)
            ai_response, response_info = self._extract_response_data(response)
            return True, ai_response, response_info
        except Exception as e:
            return False, str(e), None

    def _extract_response_data(self, response):
        urls = [item["url"] for item in response["data"]]
        ai_response = urls[0] if len(urls) == 1 else ", ".join(urls)
        response_info = {
            "Prompt tokens": None,
            "Completion tokens": None,
            "Total tokens": None
        }
        return ai_response, response_info
