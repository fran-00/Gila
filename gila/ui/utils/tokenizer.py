import math
import re


class Tokenizer:

    _PATTERN = re.compile(
        r"""
            # Number: 123, 3.14, 2,718 optionally followed by unit/currency
            \d+(?:[.,]\d+)*(?:°|º|%|‰|€|\$|£)?
            | # Word: letters (incl. accented) + any combining marks
            [A-Za-zÀ-ÖØ-öø-ÿ]+(?:[\u0300-\u036f]+[A-Za-zÀ-ÖØ-öø-ÿ]+)*
            | # Apostrophes (straight or curly)
            [’']
            | # Hyphens and dashes
            [-–—]
            | # Any other single symbol or punctuation (incl. emojis)
            [^\w\s]
            | # Whitespace
            \s+
        """,
        re.UNICODE | re.VERBOSE,
    )

    def __init__(self, avg_chars_per_token: float = 4.2, word_threshold: int = 6):
        self.avg_chars_per_token = avg_chars_per_token
        self.word_threshold = word_threshold

    def _encode(self, text: str) -> list[str]:
        pieces = re.findall(self._PATTERN, text)
        tokens: list[str] = []

        for p in pieces:
            # drop whitespace
            if p.isspace():
                continue

            # purely alphanumeric (letters or digits)
            if p[0].isalnum():
                L = len(p)
                # if the word is short enough, keep it as one token
                if L <= self.word_threshold:
                    tokens.append(p)
                else:
                    # break into roughly equal subwords
                    n_sub = max(1, math.ceil(L / self.avg_chars_per_token))
                    chunk = max(1, math.ceil(L / n_sub))
                    for i in range(0, L, chunk):
                        tokens.append(p[i : i + chunk])
            else:
                # punctuation, apostrophe or dash equals one token
                tokens.append(p)

        return tokens

    def get_num_of_tokens(self, text: str) -> int:
        """
        Return approximate token count.
        """
        return len(self._encode(text))
