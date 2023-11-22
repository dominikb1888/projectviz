import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import data as d

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    with open("templates/index.html", "r") as file:
        html_content = file.read()

    return templates.TemplateResponse(index.html, data())

@app.get("/data")
async def data():
    with open("data.json") as f:
        data = json.load(f)

    return data



