import os

import cohere
from dotenv import load_dotenv


class CohereClient:

    def __init__(self):
        self.load_api_key()
        self.chat_history = []

    def load_api_key(self):
        load_dotenv()
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))

    def submit_prompt(self, prompt):
        # generate a response with the current chat history
        response = self.co.chat(
            prompt,
            temperature=0.8,
            chat_history=self.chat_history
        )
        answer = response.text

        # add message and answer to the chat history
        user_message = {"user_name": "User", "text": prompt}
        bot_message = {"user_name": "Chatbot", "text": answer}
        
        self.chat_history.append(user_message)
        self.chat_history.append(bot_message)
        return answer
