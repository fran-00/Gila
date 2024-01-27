import os

import google.generativeai as genai
from dotenv import load_dotenv


class GoogleClient:

    def __init__(self):
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = {
            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
        }
        self.model = genai.GenerativeModel('gemini-pro',
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)
        self.chat = self.model.start_chat(history=[])
        self.load_api_key()

    def submit_prompt(self, prompt):
        response = self.chat.send_message(prompt, stream=True)
        response_text = ""
        for chunk in response:
            response_text += chunk.text
        return response_text

    def load_api_key(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
