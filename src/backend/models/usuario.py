# modelo de dados do usuário

from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int]  
    nome: str          
    email: str         
