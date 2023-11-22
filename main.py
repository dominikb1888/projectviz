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
    with open("data.json") as f:
        repos = json.load(f)
    return templates.TemplateResponse('index.html', {'request': request, 'repos': repos})

@app.get("/repos")
async def repos():
    d.get_data()
    return 'Repos updated'



