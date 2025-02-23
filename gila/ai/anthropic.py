import anthropic
from .api_client import APIClient


class AnthropicClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "ANTHROPIC"
        self.chat_history = []
        self.client = anthropic.Anthropic(api_key=self.get_api_key())

    def _get_endpoint(self):
        return "https://api.anthropic.com/v1/messages"

    def submit_prompt(self, prompt):
        self.chat_history.append(
            {"role": "user", "content": {"type": "text", "text": prompt}}
        )
        try:
            message = self.client.messages.create(
                model=self.llm,
                system="You are an helpful assistant.",
                messages=self.chat_history,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            answer = message.content
            response_info = None
            self.chat_history.append(
                {
                    "role": "assistant",
                    "content": {"text": answer, "type": "text"},
                }
            )
            return True, answer, response_info
        except anthropic.APIError as e:
            return False, e.message, None

    def _extract_response_data(self, response):
        pass

    def on_chat_reset(self):
        self.chat_history = []
        self.chat_custom_name = None
        self.generate_chat_id()

    def validate_api_key(self, api_key):
        test = anthropic.Anthropic(api_key=api_key)
        try:
            test.messages.create(messages="test", max_tokens=10, model=self.llm)
            return True
        except ValueError as e:
            return False
