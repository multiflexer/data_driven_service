import re
import spacy
from functools import lru_cache

# %pip install https://github.com/explosion/spacy-models/releases/download/ru_core_news_sm-3.4.0/
# ru_core_news_sm-3.4.0-py3-none-any.whl


class PreprocessorService:
    def __init__(self):
        self._nlp = spacy.load("ru_core_news_sm")

    def _gen_tokens(self, text: str):
        doc = self._nlp(str(text))
        for token in doc:
            if token.is_stop or token.is_punct or token.like_num or token.like_url \
                    or token.like_email or token.is_digit or len(token) <= 1 or token.is_space \
                    or not re.match(r'^[a-zA-Zа-яА-Я]+$', str(token)):
                continue
            yield token.lemma_

    def preprocess_text(self, text: str):
        return " ".join(self._gen_tokens(text))


@lru_cache
def get_preprocessor_service():
    return PreprocessorService()
