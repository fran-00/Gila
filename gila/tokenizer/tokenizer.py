import tiktoken


class Tokenizer:

    def __init__(self):
        pass

    def get_num_of_tokens(self, text):
        encoding = tiktoken.get_encoding("cl100k_base")
        encoding.encode(text)
        num_tokens = len(encoding.encode(text))
        return num_tokens
