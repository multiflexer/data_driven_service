from urllib.parse import urljoin

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from config import config

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
                                       "content_js": templates.get_template("form.js").render(
                                           post_endpoint=urljoin(config.API_BASE, "/comment"))
                                       })


@app.post("/comment")
async def comment_post(data: str = Form()):
    print("hey")
    print(data)
    return ''


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
    )
