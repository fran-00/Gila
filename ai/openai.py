import os

import openai
from dotenv import load_dotenv


class OpenAIClient:

    def __init__(self):
        self.load_api_key()
        self.prompts = [{"role": "system", "content": "You are a helpful assistant."}]

    def load_api_key(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def submit_prompt(self, prompt):
        self.prompts.append({"role": "user", "content": prompt})

        # Request gpt-3.5-turbo for chat completion
        response = openai.OpenAI().chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.prompts
        )

        # Print the response and add it to the messages list
        ai_response = response.choices[0].message.content
        self.prompts.append({"role": "assistant", "content": ai_response})
        return ai_response
