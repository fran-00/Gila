import openai

from .api_client import APIClient


class OpenAIClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "OPENAI"
        self.chat_history = [{"role": "system", "content": "You are an helpful assistant."}]

    def submit_prompt(self, prompt):
        if self.llm_name in ["DALL-E-2", "DALL-E-3"]:
            return self.on_image_generations(prompt)
        else:
            return self.on_chat_completions(prompt)

    def _get_endpoint(self):
        return "https://api.openai.com/v1/chat/completions"

    def on_chat_completions(self, prompt):
        self.chat_history.append({"role": "user", "content": prompt})
        try:
            response = self.send_request()
            response_info = {
                "Prompt tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "Completion tokens": response.get("usage", {}).get("completion_tokens", 0),
                "Total tokens": response.get("usage", {}).get("total_tokens", 0),
            }
            ai_response = response["choices"][0]["message"]["content"]
            self.chat_history.append({"role": "assistant", "content": ai_response})
            
            return True, ai_response, response_info
        except KeyError as e:
            return False, str(e), None

    def on_image_generations(self, prompt):
        endpoint = "https://api.openai.com/v1/images/generations"
        data = {
            "model": self.llm,
            "prompt": prompt,
            "n": 1,
            "size": "256x256"
        }
        try:
            response = self.send_request(endpoint, data)
            image_url = response["data"][0]["url"]
            return True, image_url, None
        except KeyError as e:
            return False, str(e), None

    def on_chat_reset(self):
        self.chat_history = [{"role": "system", "content": "You are an helpful assistant."}]
        self.chat_custom_name = None
        self.generate_chat_id()

    def validate_api_key(self, api_key):
        openai.api_key = api_key
        try:
            openai.models.list()
            return True
        except openai.AuthenticationError as e:
            print(e)
            return False
