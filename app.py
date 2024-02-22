import networkx as nx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
load_dotenv()

from mindmap_utils import CreateMindmap

app = FastAPI()


from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app.mount("/static", StaticFiles(directory="static"), name="static")  
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index2.html", {"request": request})


@app.post("/generate_mindmap")
async def generate_mindmap(request: Request):
    data = await request.json()
    text = data.get("text")

    if not text:
        return {"error": "Please provide the 'text' field"}

    mindmap_html = CreateMindmap(text)
    return HTMLResponse(content=mindmap_html)
