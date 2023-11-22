import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import data as d

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    with open("templates/index.html", "r") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content)

@app.get("/data")
async def data():
    with open("data.json") as f:
        data = json.load(f)

    return data



