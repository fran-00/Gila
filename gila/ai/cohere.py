import cohere

from .api_client import APIClient


class CohereClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "COHERE"
        self.chat_history = []

    def submit_api_key(self):
        self.co = cohere.Client(self.get_api_key())

    def submit_prompt(self, prompt):
        # FIXME: Cohere chat not working
        try:
            response = self.co.chat(
                message={prompt},
                model=self.llm,
                chat_history=self.chat_history,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            answer = response.text
            response_info = None
            user_message = {"role": "User", "message": prompt}
            bot_message = {"role": "Chatbot", "message": answer}

            self.chat_history.append(user_message)
            self.chat_history.append(bot_message)
            return True, answer, response_info
        except cohere.error.CohereConnectionError as e:
            return False, e.message, None

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
