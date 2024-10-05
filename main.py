from sqlite3 import IntegrityError
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from models.usuario_model import Usuario
from repositories import usuario_repo

usuario_repo.criar_tabela()
usuario_repo.insere_dados_interesse()

app = FastAPI()

template = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def get_root(request: Request):
    return template.TemplateResponse("index.html", {"request": request})

@app.get("/cadastro")
def  get_cadastro(request: Request):
   return template.TemplateResponse("form_registro.html", {"request": request})

@app.post("/post_cadastro")
def post_cadastro(
   request: Request,
   nome: str = Form(...),
   email: str = Form(...),
   telefone: str = Form(...),
   data_nascimento: str = Form(...),
   senha: str = Form(...),
   confirmar_senha: str = Form(...)):
   if senha != confirmar_senha:
      #cadastrar_contato(nome, data_nasc, telefone, email, senha)
      return  template.TemplateResponse("/cadastro?error=senhas_diferentes", 303)
   usuario = Usuario(None, nome, email, telefone, data_nascimento, senha)
   try:
      usuario_id = usuario_repo.inserir(usuario)
      return RedirectResponse(f"/interesses?user_id={usuario_id}", 303)
   except IntegrityError:
      return template.TemplateResponse("/cadastro?error=usuario_ja_cadastrado", 303)
   except Exception as e:
      return template.TemplateResponse("/cadastro?error=erro_ao_cadastrar", 303)

   #    if usuario:
   #       return RedirectResponse(f"/interesses?user_id", 303)
      
   #    else:
   #       return RedirectResponse("/cadastro", 303)
   # else:
   #    return RedirectResponse("/cadastro", 303)

# @app.post("/intesses")
# def post_interesses(request: Request, interesses: str = Form(...)):

@app.get("/login")
def get_login(request: Request):
   return template.TemplateResponse("login.html", {"request": request})


if __name__ == "__main__":
 uvicorn.run("main:app", port=8000, reload=True)