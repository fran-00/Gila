import openai

from .api_client import APIClient


class OpenAIClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "OPENAI"
        self.temperature = 0.7
        self.chat_history = [{"role": "system", "content": "You are a helpful assistant."}]

    def submit_api_key(self):
        openai.api_key = self.get_api_key()

    def submit_prompt(self, prompt):
        self.chat_history.append({"role": "user", "content": prompt})
        try:
            response = openai.OpenAI().chat.completions.create(
                model=self.llm,
                messages=self.chat_history
            )

            ai_response = response.choices[0].message.content
            self.chat_history.append({"role": "assistant", "content": ai_response})
            return True, ai_response
        except openai.APIError as e:
            return False, e.message

    def on_chat_reset(self):
        self.chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
        self.generate_chat_id()

    def validate_api_key(self, api_key):
        openai.api_key = api_key
        try:
            openai.models.list()
            return True
        except openai.AuthenticationError as e:
            print(e)
            return False
