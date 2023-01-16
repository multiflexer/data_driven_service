import os
import pickle
from functools import lru_cache

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

from config import config


class ModelService:
    class_mapping = {1: "POSITIVE", 0: "NEGATIVE"}

    def __init__(self):
        with open(os.path.join(config.ML_BASE_DIR, config.PATH_TO_MODEL_PICKLE), 'rb') as f:
            self.model: LogisticRegression = pickle.load(f)

    def predict(self, vec: TfidfVectorizer):
        result = self.model.predict(vec)[0]
        return self.class_mapping[result]


@lru_cache
def get_model_service():
    return ModelService()
