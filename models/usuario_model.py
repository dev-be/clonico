from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Usuario:
    id_usuario: Optional[int] = None
    nome: Optional[str]  = None
    email: Optional[str]  = None
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    senha: Optional[str] = None

@dataclass
class Iteresses:
    id: Optional[int] = None
    usuario:  Optional[Usuario] = None
    interesse:  Optional[str] = None