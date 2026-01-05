# responsável por deletar dados
from database import get_connection 

def deletar_conta(conta_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM contas WHERE id = ?",
            (conta_id,)
        )
        conn.commit()
