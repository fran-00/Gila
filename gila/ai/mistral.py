import mistralai
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
        endpoint = "https://api.mistral.ai/v1/chat/completions"
        data = {
            "model": self.llm,
            "messages": self.chat_history,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        try:
            response = self.send_request(endpoint, data)
            response_info = {
                "Prompt tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "Completion tokens": response.get("usage", {}).get("completion_tokens", 0),
                "Total tokens": response.get("usage", {}).get("total_tokens", 0),
            }
            ai_response = response["choices"][0]["message"]["content"]
            self.chat_history.append({"role": "assistant", "content": ai_response})

            return True, ai_response, response_info
        except KeyError as e:
            return False, str(e), None

    def on_chat_reset(self):
        self.chat_history = [{"role": "system", "content": "You are an helpful assistant."}]
        self.chat_custom_name = None
        self.generate_chat_id()

    def validate_api_key(self, api_key):
        test = mistralai.Mistral(api_key)
        try:
            test.chat.complete(model = self.llm, messages=[{"role": "user", "content": "test"}])
            return True
        except mistralai.models.sdkerror.SDKError as e:
            return False
