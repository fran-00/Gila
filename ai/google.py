import google.generativeai as genai

from .api_client import APIClient


class GoogleClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.temperature = 0.7
        generation_config = {
            "temperature": self.temperature,
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
        self.model = genai.GenerativeModel(self.llm,
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)
        self.chat_messages = self.model.start_chat(history=[])

        genai.configure(api_key=self.load_api_key("GOOGLE"))

    def submit_prompt(self, prompt):
        response = self.chat_messages.send_message(prompt, stream=True)
        response_text = ""
        for chunk in response:
            response_text += chunk.text
        return response_text
