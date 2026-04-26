from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os

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
# ROTAS DO FRONTEND
# ==========================================
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend')


@app.route('/')
def index():
    return send_from_directory(FRONTEND_PATH, 'usuario.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(FRONTEND_PATH, filename)

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

        resultado = []
        for c in contas:
            # trata o vencimento (string ou date)
            venc = c.vencimento
            if hasattr(venc, 'isoformat'):
                venc = venc.isoformat()

            resultado.append({
                "id": c.id,
                "descricao": c.descricao,
                "valor": float(c.valor),
                "vencimento": venc,
                "tipo": c.tipo.value if hasattr(c.tipo, "value") else c.tipo,
                "sincronizado": bool(c.sincronizado)
            })

        print(f"📤 {len(resultado)} contas enviadas para o frontend.")
        return jsonify(resultado), 200

    except Exception as e:
        print("❌ ERRO AO LISTAR CONTAS:", e)
        return jsonify([]), 500
    
# ==========================================
# ROTA: REGISTRAR USUÁRIO
# ==========================================
@app.route('/api/usuarios', methods=['POST'])
def registrar_usuario():
    dados = request.get_json()
    try:
        nome = dados.get('nome')
        email = dados.get('email')
        criar_usuario(nome, email)
        return jsonify({"success": True}), 200
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return jsonify({"success": True, "message": "Usuário já existe"}), 200
        return jsonify({"success": False, "error": str(e)}), 500

# ==========================================
# ROTA: DELETAR CONTA
# ==========================================
@app.route('/api/contas/<int:conta_id>', methods=['DELETE'])
def deletar_conta(conta_id):
    try:
        from crud.delete import deletar_conta_por_id
        deletar_conta_por_id(conta_id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ==========================================
# EXECUÇÃO LOCAL
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
