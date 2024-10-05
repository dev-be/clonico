from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from sqlalchemy import Session
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
   if senha == confirmar_senha:
      #cadastrar_contato(nome, data_nasc, telefone, email, senha)
      usuario = Usuario(None, nome, email, telefone, data_nascimento, senha)
      usuario_repo.inserir(usuario)
      if usuario:
         return RedirectResponse(f"/interesses", 303)
      
      else:
         return RedirectResponse("/cadastro", 303)
   else:
      return RedirectResponse("/cadastro", 303)
   
@app.get("/interesses")
def get_interesses(request: Request):
   return template.TemplateResponse("form_interesse.html", {"request": request})

# @app.post("/post_intesses")
# def post_interesses(request: Request, interesses: str = Form(...)):

@app.get("/login")
def get_login(request: Request):
   return template.TemplateResponse("login.html", {"request": request})

# @app.post("/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = usuario_repo.get_user(form_data.username)
#     if not user or not usuario_repo.verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials",
#             headers={"WWW-Authenticate": "Basic"},
#         )
    
#     return {"message": "Login bem-sucedido!"}

if __name__ == "__main__":
 uvicorn.run("main:app", port=8000, reload=True)