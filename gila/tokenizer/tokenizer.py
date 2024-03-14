import tiktoken


class Tokenizer:

    def __init__(self):
        pass

    def tokens_counter(self, text):
        encoding = tiktoken.get_encoding("cl100k_base")
        encoding.encode(text)
        num_tokens = len(encoding.encode(text))
        return num_tokens
