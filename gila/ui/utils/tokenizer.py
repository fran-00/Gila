import math
import re


class Tokenizer:

    def __init__(self, avg_chars_per_token: float = 4.2, word_threshold: int = 6):
        self.avg_chars_per_token = avg_chars_per_token
        self.word_threshold = word_threshold

    def get_num_of_tokens(self, text):
        pass
