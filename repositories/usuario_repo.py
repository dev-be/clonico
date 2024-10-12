from typing import List, Optional
from models.usuario_model import Usuario, Interesses, Profile, InteressesProfile
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
        db.execute(SQL_INSERIR_USUARIO, (
            usuario.nome, 
            usuario.username,
            usuario.email,
            usuario.telefone, 
            usuario.data_nascimento, 
            usuario.senha
        ))

        if db.rowcount > 0:
            usuario.id_usuario = db.lastrowid
            print(f"{usuario}")
            return usuario.id_usuario
        else:
            return None
        
def email_existe(email: str) -> bool:
    with obter_conexao() as conexao:
        db = conexao.cursor()
        db.execute(SQL_EMAIL_EXISTE, (email,))
        return db.fetchone() is not None
    
def username_existe(username:  str) -> bool:
    with obter_conexao() as conexao:
        db = conexao.cursor()
        db.execute(SQL_USERNAME_EXISTE, (username,))
        return db.fetchone() is not None


def insere_interesse_usuario(interesse: Interesses) -> Optional[Interesses]:
    with obter_conexao() as conexao:
        db = conexao.cursor()
        db.execute(SQL_SALVAR_INTERESSE, (
             interesse.usuario, 
             interesse.interesse
             ))
        conexao.commit()

def obter_usuario_por_email_username(identifier: str) -> Optional[Usuario]:
    with obter_conexao() as conexao:
        db = conexao.cursor()
        db.execute(SQL_OBTER_USUARIO_POR_EMAIL_USERNAME, (identifier, identifier))
        resultado = db.fetchone()
        if resultado:
            return Usuario(*resultado)
        else:
            return None
        
def verificar_senha(senha_fornecida: str, senha_armazenada: str) -> bool:
    return senha_fornecida == senha_armazenada

def obter_dados_usuario(usuario_id: int) -> Profile:
    with obter_conexao() as conexao:
        db = conexao.cursor()
        db.execute(SQL_OBTER_DADOS_USUARIO, (usuario_id,))
        resultado = db.fetchone()
        if resultado:
            return Profile(id_usuario=resultado[0], nome=resultado[1])
        return None

def obter_interesses_usuario(usuario: int) -> List[InteressesProfile]:
    with obter_conexao() as conexao:
        db = conexao.cursor()
        db.execute(SQL_EXIBIR_USER_PROFILE, (usuario,))
        resultado = db.fetchall()
        return [InteressesProfile(usuario=usuario, interesse=row[1]) for row in resultado]
