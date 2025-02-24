from .api_client import APIClient


class ArliClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "ARLI"

    def _get_endpoint(self):
        return "https://api.arliai.com/v1/chat/completions"
