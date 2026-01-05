from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Importações do projeto
from crud.create import criar_usuario, criar_conta
from crud.read import listar_contas_usuario
from database import init_db
from main import criar_lembrete_google
from models.conta import Conta, TipoConta

# ==========================================
# CONFIGURAÇÃO DO FLASK
# ==========================================
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Inicializa o banco (cria tabelas se necessário)
init_db()

# ==========================================
# ROTA: REGISTRAR CONTA
# ==========================================
@app.route('/api/contas', methods=['POST', 'OPTIONS'])
def registrar():
    if request.method == 'OPTIONS':
        return jsonify({"success": True}), 200

    dados = request.get_json()
    print(f"📥 Dados recebidos: {dados}")

    try:
        # --- Tratamento dos dados recebidos ---
        valor = float(str(dados.get('valor', '0')).replace(',', '.'))
        descricao = dados.get('descricao', 'Sem descrição')
        data_venc = dados.get('data')
        usuario_id = int(dados.get('usuario_id', 1))
        modalidade = dados.get('modalidade', 'esporadica').lower()

        tipo_conta = TipoConta(modalidade)

        # --- Cria objeto Conta ---
        conta = Conta(
            id=None,
            usuario_id=usuario_id,
            descricao=descricao,
            valor=valor,
            vencimento=datetime.strptime(data_venc, '%Y-%m-%d').date(),
            tipo=tipo_conta,
            sincronizado=True
        )

        # --- Salva no banco ---
        criar_conta(conta)

        # --- Integração opcional com Google Agenda ---
        try:
            criar_lembrete_google(descricao, data_venc, valor)
        except Exception as e:
            print("⚠️ Google Agenda indisponível:", e)

        print("✅ Conta registrada com sucesso.")
        return jsonify({"success": True, "message": "Conta registrada com sucesso!"}), 200

    except Exception as e:
        print(f"❌ ERRO AO REGISTRAR: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ==========================================
# ROTA: LISTAR CONTAS DE UM USUÁRIO
# ==========================================
@app.route('/api/contas/<int:usuario_id>', methods=['GET'])
def listar_contas(usuario_id):
    try:
        contas = listar_contas_usuario(usuario_id)

        # Converte objetos Conta em JSON
        resultado = []
        for c in contas:
            resultado.append({
                "id": c.id,
                "descricao": c.descricao,
                "valor": c.valor,
                "vencimento": c.vencimento.isoformat(),
                "tipo": c.tipo.value if hasattr(c.tipo, "value") else c.tipo,
                "sincronizado": c.sincronizado
            })

        print(f"📤 {len(resultado)} contas enviadas para o frontend.")
        return jsonify(resultado), 200

    except Exception as e:
        print("❌ ERRO AO LISTAR CONTAS:", e)
        return jsonify([]), 500


# ==========================================
# EXECUÇÃO LOCAL
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
