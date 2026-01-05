# responsável por buscar dados

from database import (
    buscar_todos_usuarios,
    buscar_usuario_por_id,
    buscar_contas_por_usuario
)

def listar_usuarios():
    return buscar_todos_usuarios()


def obter_usuario(usuario_id: int):
    return buscar_usuario_por_id(usuario_id)


def listar_contas_usuario(usuario_id: int):
    return buscar_contas_por_usuario(usuario_id)
