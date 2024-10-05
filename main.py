from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


app = FastAPI()

template = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def get_root(request: Request):
    return template.TemplateResponse("index.html", {"request": request})

@app.get("/cadastro")
def  get_cadastro(request: Request):
   return template.TemplateResponse("form_registro.html", {"request": request})

@app.get("/login")
def get_login(request: Request):
   return template.TemplateResponse("login.html", {"request": request})


if __name__ == "__main__":
 uvicorn.run("main:app", port=8000, reload=True)