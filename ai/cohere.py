import cohere

from .api_client import APIClient


class CohereClient(APIClient):

    def __init__(self):
        self.temperature = 0.8
        self.chat_messages = []
        self.co = cohere.Client(self.load_api_key("COHERE"))

    def submit_prompt(self, prompt):
        # generate a response with the current chat history
        response = self.co.chat(
            prompt,
            temperature=0.8,
            chat_history=self.chat_messages
        )
        answer = response.text

        # add message and answer to the chat history
        user_message = {"user_name": "User", "text": prompt}
        bot_message = {"user_name": "Chatbot", "text": answer}

        self.chat_messages.append(user_message)
        self.chat_messages.append(bot_message)
        return answer

    def on_chat_reset(self):
        self.chat_messages = []
