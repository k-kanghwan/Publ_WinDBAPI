from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from database.database import Base, engine
from controllers.controllers import router


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
Base.metadata.create_all(bind=engine)
app.include_router(router)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
