from .api_client import APIClient


class MistralClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "MISTRAL"
        self.chat_history = [{"role": "system", "content": "You are an helpful assistant."}]

    def _get_endpoint(self):
        return "https://api.mistral.ai/v1/chat/completions"

    def submit_prompt(self, prompt):
        self.chat_history.append({"role": "user", "content": prompt})
        try:
            response = self.send_request()
            ai_response, response_info = self._extract_response_data(response)
            self.chat_history.append({"role": "assistant", "content": ai_response})
            return True, ai_response, response_info
        except KeyError as e:
            return False, str(e), None

    def _extract_response_data(self, response):
        ai_response = response["choices"][0]["message"]["content"]
        response_info = {
            "Prompt tokens": response.get("usage", {}).get("prompt_tokens", 0),
            "Completion tokens": response.get("usage", {}).get("completion_tokens", 0),
            "Total tokens": response.get("usage", {}).get("total_tokens", 0),
        }
        return ai_response, response_info

    def on_chat_reset(self):
        self.chat_history = [{"role": "system", "content": "You are an helpful assistant."}]
        self.chat_custom_name = None
        self.generate_chat_id()
