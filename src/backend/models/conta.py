# modelo de dados da conta

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class TipoConta(str, Enum):
    FIXA = "fixa"
    ESPORADICA = "esporadica"
    PARCELADA = "parcelada"


@dataclass
class Conta:
    id: Optional[int]              # gerado automaticamente pelo banco
    usuario_id: int                # foreign key → Usuario.id
    descricao: str                 # exemplo: "Conta de luz"
    valor: float                   # valor da conta
    vencimento: date               # data de vencimento
    tipo: TipoConta                # tipo da conta
    parcela_atual: int = 1         # parcela atual (se parcelada)
    total_parcelas: int = 1        # total de parcelas
    sincronizado: bool = False     # já foi enviada ao Google Calendar?
 