import sys
from urllib.parse import urljoin
from http import HTTPStatus

import uvicorn
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from config import config
from schemas.api import ResponsePredict
from ml_services.model_service import get_model_service, ModelService
from ml_services.preprocessor_service import get_preprocessor_service, PreprocessorService
from ml_services.vectorizer_service import get_vectorizer_service, VectorizerService

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/css", StaticFiles(directory="./static"), name="css")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "example_data": "Всё хорошо, прекрасная маркиза!",
                                       "content_js": templates.get_template("form.js").render(
                                           post_endpoint=urljoin(config.API_BASE, "/comment"))
                                       })


@app.post("/comment", response_model=ResponsePredict)
def comment_post(data: str = Form(),
                 model_service: ModelService = Depends(get_model_service),
                 vectorizer_service: VectorizerService = Depends(get_vectorizer_service),
                 preprocessor_service: PreprocessorService = Depends(get_preprocessor_service)):
    try:
        preprocessed_text = preprocessor_service.preprocess_text(data)
        vectorized_text = vectorizer_service.vectorize(preprocessed_text)
        class_result = model_service.predict(vectorized_text)
    except Exception as e:
        print(e, file=sys.stderr)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Something went wrong")
    return ResponsePredict(class_name=class_result)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
    )
