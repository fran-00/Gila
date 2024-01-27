import os

import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class GoogleClient:
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])

    def submit_prompt(self, prompt):
        response = self.chat.send_message(prompt, stream=True)
        response_text = ""
        for chunk in response:
            response_text += chunk.text
        return response_text
