from fastapi import HTTPException, Request
from auth.cookies import serializer
from repositories import usuario_repo


def get_current_user(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=403, detail="Not authenticated")

    try:
        user_id = serializer.loads(session_token)
        usuario = usuario_repo.obter_dados_usuario(user_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return usuario
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid session")