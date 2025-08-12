from fastapi import FastAPI
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root():
    return templates.TemplateResponse("home.html", {"request": {}})


@app.get("/about")
def read_about():
    return templates.TemplateResponse("about.html", {"request": {}})
