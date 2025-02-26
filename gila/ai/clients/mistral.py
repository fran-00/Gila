from ..api_client import APIClient


class MistralClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "MISTRAL"

    def _get_endpoint(self):
        return "https://api.mistral.ai/v1/chat/completions"

