import os

from dotenv import load_dotenv


class APIClient:

    def __init__(self, llm=None):
        self.llm = llm
        self.llm_name = None
        self.temperature = None

    def load_api_key(self, name):
        load_dotenv()
        return os.getenv(f"{name}_API_KEY")
