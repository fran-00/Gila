from ..api_client import APIClient


class DeepSeekClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "DEEPSEEK"

    def _get_endpoint(self):
        return "https://api.deepseek.com/chat/completions"
