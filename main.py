import re
from typing import Optional
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from sqlalchemy import Session
import uvicorn

from auth.cookies import create_token, decode_token, remover_cookies
from models.usuario_model import Usuario, Interesses
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
   username: str = Form(...),
   email: str = Form(...),
   telefone: str = Form(...),
   data_nascimento: str = Form(...),
   senha: str = Form(...),
   confirmar_senha: str = Form(...)):
   if senha != confirmar_senha:
        return RedirectResponse("/cadastro?error=senhas_diferentes", status_code=303)

   if usuario_repo.email_existe(email):
        return RedirectResponse("/login?error=email_ja_cadastrado", status_code=303)
   
   if usuario_repo.username_existe(username):
       return RedirectResponse("/cadastro?error=username_ja_cadastrado", status_code=303)
   
   if not re.match(r'^[a-z0-9_]+$', username):
       return RedirectResponse("/cadastro?error=nome_usuario_invalido", status_code=303)

   usuario = Usuario(None, nome, username, email, telefone, data_nascimento, senha)

   try:
      usuario_id = usuario_repo.inserir(usuario)
      session_token = create_token(str(usuario_id))
      response = RedirectResponse("/interesses",  status_code=303)
      response.set_cookie(key="session_token", value=session_token, httponly=True)
      return response

   except Exception as e:
      return RedirectResponse("/cadastro?error=erro_inesperado", status_code=303)
   
@app.get("/interesses")
def get_interesses(request: Request):
   session_token: Optional[str] = request.cookies.get("session_token")
   if session_token is None:
      return RedirectResponse("/cadastro", status_code=303)
   return template.TemplateResponse("form_interesse.html", {"request": request})

@app.post("/post_interesses")
def post_interesses(
    request: Request,
    interesses: tuple = Form(...)):
    session_token: Optional[str] = request.cookies.get("session_token")

    if session_token is None:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    usuario_id = decode_token(session_token)

    if usuario_id is None:
        raise HTTPException(status_code=401, detail="Token de sessão inválido ou expirado")

    for interesse in interesses:
        usuario_repo.insere_interesse_usuario(Interesses(None, usuario_id, interesse))

    return RedirectResponse("/login", status_code=303)

@app.get("/login")
def get_login(request: Request):
   return template.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(
   request: Request,
   identifier: str = Form(...),
   senha: str = Form(...)):

   usuario = usuario_repo.obter_usuario_por_email_username(identifier)

   if not usuario or not usuario_repo.verificar_senha(senha,  usuario.senha):
      return RedirectResponse("/login?error=credenciais_invalidas", status_code=303)
   
   session_token  = create_token(str(usuario.id_usuario))
   response  = RedirectResponse("/feed?message=login_efetuado_com_sucesso",  status_code=303)
   response.set_cookie(key="session_token", value=session_token, httponly=True)
   return response

@app.get("/logout")
def logout(request: Request):
    response = RedirectResponse("/login", status_code=303)
    remover_cookies(response)
    return response

@app.get("/feed")
def get_root(request: Request):
    return template.TemplateResponse("feed.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
def get_profile(request: Request):
    session_token = request.cookies.get("session_token")

    if not session_token:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    usuario_id = decode_token(session_token)

    if usuario_id is None:
        raise HTTPException(status_code=401, detail="Token de sessão inválido ou expirado")

    usuario = usuario_repo.obter_dados_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    interesses = usuario_repo.obter_interesses_usuario(usuario_id)


    return  template.TemplateResponse("perfil.html", {
        "request": request,
        "usuario": usuario,
        "interesses": interesses
    })

if __name__ == "__main__":
 uvicorn.run("main:app", port=8000, reload=True)