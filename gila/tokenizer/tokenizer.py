import tiktoken


class Tokenizer:

    def __init__(self):
        pass

    def encode(self, text, encoding_model):
        encoding = tiktoken.encoding_for_model(encoding_model)
        encoding.encode(text)
        num_tokens = len(encoding.encode(text))
        return num_tokens
