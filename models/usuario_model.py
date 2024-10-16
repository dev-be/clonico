from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Usuario:
    id_usuario: Optional[int] = None
    nome: Optional[str]  = None
    username: Optional[str] = None
    email: Optional[str]  = None
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    senha: Optional[str] = None

@dataclass
class Interesses:
    id: Optional[int] = None
    usuario:  Optional[str] = None
    interesse:  Optional[str] = None

@dataclass
class Login:
    usuario: Optional[str] =  None
    senha: Optional[str] = None

@dataclass
class Profile:
    id_usuario: Optional[int] = None
    nome: Optional[str] = None
    username: Optional[str] = None

@dataclass
class InteressesProfile:
        usuario: Optional[int] =  None
        interesse: Optional[int] =  None
