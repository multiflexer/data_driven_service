import os
import pickle
from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer

from config import config


class VectorizerService:
    def __init__(self):
        with open(os.path.join(config.ML_BASE_DIR, config.PATH_TO_VECTORIZER_PICKLE), 'rb') as f:
            self.vectorizer: TfidfVectorizer = pickle.load(f)

    def vectorize(self, pre_processed_text: str):
        result = self.vectorizer.transform([pre_processed_text])
        return result


@lru_cache
def get_vectorizer_service():
    return VectorizerService()
