import openai

from .api_client import APIClient


class OpenAIClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.temperature = 0.7
        self.chat_messages = [{"role": "system", "content": "You are a helpful assistant."}]
        openai.api_key = self.load_api_key("OPENAI")

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
