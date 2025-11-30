from ..api_client import APIClient


class LMStudioClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "LMSTUDIO"

    def _get_endpoint(self):
        return "http://127.0.0.1:1234/v1/chat/completions"

