import cohere

from .api_client import APIClient


class CohereClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "COHERE"
        self.temperature = 0.8
        self.chat_history = []

    def submit_api_key(self):
        self.co = cohere.Client(self.get_api_key())

    def submit_prompt(self, prompt):
        try:
            response = self.co.chat(
                prompt,
                temperature=self.temperature,
                chat_history=self.chat_history
            )
            answer = response.text
            user_message = {"user_name": "User", "text": prompt}
            bot_message = {"user_name": "Chatbot", "text": answer}

            self.chat_history.append(user_message)
            self.chat_history.append(bot_message)
            return True, answer
        except cohere.error.CohereConnectionError as e:
            return False, e.message

    def on_chat_reset(self):
        self.chat_history = []
        self.chat_custom_name = None
        self.generate_chat_id()

    def validate_api_key(self, api_key):
        test_co = cohere.Client(api_key)
        try:
            test_co.generate(prompt='test')
            return True
        except cohere.CohereError as e:
            return False
