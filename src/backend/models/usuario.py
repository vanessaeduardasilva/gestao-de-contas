# modelo de dados do usuário

from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int]  # gerado automaticamente pelo banco
    nome: str          # nome do usuário
    email: str         # email único (usado para login/validação)
