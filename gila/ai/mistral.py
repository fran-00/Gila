from .api_client import APIClient


class MistralClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "MISTRAL"
        self.chat_history = [{"role": "system", "content": "You are an helpful assistant."}]

    def _get_endpoint(self):
        return "https://api.mistral.ai/v1/chat/completions"

    def on_chat_reset(self):
        self.chat_history = [{"role": "system", "content": "You are an helpful assistant."}]
        self.chat_custom_name = None
        self.generate_chat_id()
