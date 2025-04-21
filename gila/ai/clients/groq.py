from ..api_client import APIClient


class GroqClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "GROQ"

    def _get_endpoint(self):
        return "https://api.groq.com/openai/v1/chat/completions"
