from typing import List, Optional
from models.post_model import Post
from sql.posts_sql import *
from util import obter_conexao

def criar_tabela_posts():
    with obter_conexao() as conexao:
        db = conexao.cursor()
        db.execute(SQL_CRIAR_TABELA_POSTAGENS)
        conexao.commit()

def inserir_post(post: Post) -> Optional[Post]:
    with obter_conexao() as conexao:
        db = conexao.cursor()
        db.execute(SQL_INSERIR_POST, (
                   post.usuario_id,
                   post.titulo,
                   post.imagem
                   ))
        conexao.commit()
        return post
    
def obter_posts() -> List[Post]:
    with obter_conexao() as conexao:
        db = conexao.cursor()
        db.execute(SQL_OBTER_POSTS)
        rows = db.fetchall()
        return [
            {
                "usuario_id": row[0],
                "username": row[1],
                "titulo": row[2],
                "imagem": row[3]
            } for row in rows
        ]
