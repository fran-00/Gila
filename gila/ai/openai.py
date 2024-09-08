import openai

from .api_client import APIClient


class OpenAIClient(APIClient):

    def __init__(self, llm):
        super().__init__(llm)
        self.company = "OPENAI"
        self.chat_history = [{"role": "system", "content": "You are an helpful assistant."}]

    def submit_api_key(self):
        openai.api_key = self.get_api_key()

    def submit_prompt(self, prompt):
        if self.llm_name in ["DALL-E-2", "DALL-E-3"]:
            return self.on_image_generations(prompt)
        else:
            return self.on_chat_completions(prompt)

    def on_chat_completions(self, prompt):
        self.chat_history.append({"role": "user", "content": prompt})
        try:
            response = openai.OpenAI().chat.completions.create(
                model=self.llm,
                messages=self.chat_history,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            response_info = {
                "Prompt tokens": response.usage.prompt_tokens,
                "Completion tokens": response.usage.completion_tokens,
                "Total tokens": response.usage.total_tokens,
            }
            ai_response = response.choices[0].message.content
            self.chat_history.append({"role": "assistant", "content": ai_response})
            return True, ai_response, response_info
        except openai.APIError as e:
            return False, e.message, None

    def on_image_generations(self, prompt):
        try:
            response = openai.OpenAI().images.generate(
                model=self.llm,
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            ai_response = response.data[0].url
            return True, ai_response, None
        except openai.APIError as e:
            return False, e.message, None

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
