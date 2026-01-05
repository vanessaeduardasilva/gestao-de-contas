# responsável por criar dados no banco

from database import salvar_usuario_no_banco, salvar_conta_no_banco
from models.usuario import Usuario
from models.conta import Conta


def criar_usuario(nome: str, email: str) -> int:
    # cria um objeto Usuario usando o model
    usuario = Usuario(
        id=None,        # será gerado pelo banco
        nome=nome,
        email=email
    )

    return salvar_usuario_no_banco(usuario)


def criar_conta(conta: Conta) -> None:
    salvar_conta_no_banco(conta)

