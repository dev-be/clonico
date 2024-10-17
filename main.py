import os
import re
import shutil
from typing import Optional
import uuid
from fastapi import Depends, FastAPI, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from auth.cookies import create_token, decode_token, remover_cookies
from auth.security_login import get_current_user
from auth.security_post import validation_post_success
from models.post_model import Post
from models.usuario_model import Usuario, Interesses
from repositories import usuario_repo
from repositories import posts_repo


usuario_repo.criar_tabela()
usuario_repo.insere_dados_interesse()
posts_repo.criar_tabela_posts()

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

   if usuario is None:
       return  RedirectResponse("/cadastro?error=usuario_nao_cadastrado", status_code=303)

   if not usuario_repo.verificar_senha(senha,  usuario.senha):
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
    posts = posts_repo.obter_posts()
    return template.TemplateResponse("feed.html", {"request": request, "posts": posts})

@app.post("/post_feed")
async def post_feed(
    request: Request,
    usuario_id: int = Depends(validation_post_success),
    titulo: str = Form(...),
    imagem: UploadFile = Form(...)):
    if usuario_id is None:
        return RedirectResponse(url="/login?usuario_desconectado", status_code=303)

    if imagem:
        unique_id =  uuid.uuid4()
        extension = imagem.filename.split(".")[-1]
        filename = f"{unique_id}.{extension}"
        file_location = f"static/images/posts/{filename}"

        directory = os.path.dirname(file_location)
        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(imagem.file, buffer)
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": f"Erro ao salvar a imagem: {str(e)}"})

        post = Post(usuario_id=usuario_id, titulo=titulo,  imagem=file_location)
        posts_repo.inserir_post(post)
    
    return RedirectResponse(url="/feed", status_code=303)

@app.get("/profile")
def get_profile(
    request: Request,
    usuario: Usuario = Depends(get_current_user)):

    if usuario:

        interesses = usuario_repo.obter_interesses_usuario(usuario.id_usuario)
    
        return template.TemplateResponse("perfil.html", {
            "request": request,
            "usuario": usuario,
            "interesses": interesses
        })

    return RedirectResponse(url="/login?usuario_desconectado", status_code=303)

if __name__ == "__main__":
 uvicorn.run("main:app", port=8000, reload=True)