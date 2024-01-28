import os

from dotenv import load_dotenv


class APIClient:
    def __init__(self):
        self.temperature = None
        self.llm = None

    def load_api_key(self, name):
        load_dotenv()
        return os.getenv(f"{name}_API_KEY")
