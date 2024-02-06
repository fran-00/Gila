import openai

from .api_client import APIClient


class OpenAIClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "OPENAI"
        self.temperature = 0.7
        self.chat_messages = [{"role": "system", "content": "You are a helpful assistant."}]

    def submit_api_key(self):
        openai.api_key = self.get_api_key()

    def submit_prompt(self, prompt):
        self.chat_messages.append({"role": "user", "content": prompt})

        # Request gpt-3.5-turbo for chat completion
        response = openai.OpenAI().chat.completions.create(
            model=self.llm,
            messages=self.chat_messages
        )

        # Print the response and add it to the messages list
        ai_response = response.choices[0].message.content
        self.chat_messages.append({"role": "assistant", "content": ai_response})
        return ai_response

    def on_chat_reset(self):
        self.chat_messages = [{"role": "system", "content": "You are a helpful assistant."}]
