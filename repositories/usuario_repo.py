from typing import Optional
from models.usuario_model import Usuario
from sql.usuario_sql import *
from util import obter_conexao


def criar_tabela():
    with obter_conexao() as conexao:
        db = conexao.cursor()
        for query in SQL_CRIAR_TABELA:
            db.execute(query)
        conexao.commit()

def insere_dados_interesse():
    with obter_conexao() as conexao:
        db = conexao.cursor()
        interesses = [
            'RPG', 'FPS', 'MOBA', 'Estratégia', 'Simulação',
            'Esportes', 'Corrida', 'Aventura', 'Puzzle',
            'Ação', 'MMO', 'Indie', 'Retro', 'Battle Royale',
            'Sandbox', 'Survival', 'Horror', 'Plataforma', 
            'Luta', 'Música'
        ]
        for interesse in interesses:
            db.execute(SQL_INSERIR_INTERESSE, (interesse, interesse))
        conexao.commit()

def inserir(usuario: Usuario) -> Optional[Usuario]:
    with obter_conexao() as conexao:
        db = conexao.cursor()
        db.execute(SQL_INSERIR, (
            usuario.nome, 
            usuario.email,
            usuario.telefone, 
            usuario.data_nascimento, 
            usuario.senha
        ))

        if db.rowcount > 0:
            usuario.id = db.lastrowid
            return usuario
        else:
            return None