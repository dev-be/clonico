from dataclasses import dataclass
from typing import Optional


@dataclass
class Post:
    usuario_id: Optional[int]  = None
    titulo: Optional[str]  = None
    imagem: Optional[str]  = None