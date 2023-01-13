from pathlib import Path

from pydantic import BaseSettings


class Config(BaseSettings):
    ML_BASE_DIR: str = str(Path(__file__).parent.parent.parent)
    PATH_TO_MODEL_PICKLE: str = "objects/model.pickle"
    PATH_TO_VECTORIZER_PICKLE: str = "objects/vectorizer.pickle"

    API_BASE: str = "http://192.168.0.105:5000"
