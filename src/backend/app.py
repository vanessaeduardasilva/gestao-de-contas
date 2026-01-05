from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from crud.create import criar_usuario, criar_conta
from crud.read import listar_contas_usuario, obter_usuario
from database import buscar_usuario_por_email  
from crud.delete import deletar_conta
from crud.uptade import atualizar_conta 

from main import criar_lembrete_google, get_calendar_service
from database import init_db
from models.conta import Conta
app = Flask(__name__)
CORS(app)

init_db()

@app.route('/api/vincular', methods=['POST'])
def vincular():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')

    try:
        # 1. Busca se o usuário existe usando seu CRUD de Read
        usuario_existente = buscar_usuario_por_email(email)
        
        if not usuario_existente:
            # 2. Se não existir, usa seu CRUD de Create (Gera ID Automático)
            user_id = criar_usuario(nome, email)
        else:
            user_id = usuario_existente['id']

        # 3. Inicia a autenticação do Google (Abre o navegador)
        get_calendar_service() 
        
        return jsonify({
            "success": True, 
            "user_id": user_id, 
            "message": "Usuário vinculado com sucesso"
        }), 200

    except Exception as e:
        print(f"Erro ao vincular: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/registrar-conta', methods=['POST'])
def registrar():
    dados = request.json
    try:
        # 1. Cria o objeto usando seu Model real
        nova_conta = Conta(
            id=None,
            usuario_id=dados.get('usuario_id'),
            descricao=dados.get('descricao'),
            valor=float(dados.get('valor')),
            # Converte a string do formulário para objeto date
            vencimento=datetime.strptime(dados.get('data'), '%Y-%m-%d').date(),
            tipo="PAGAMENTO",
            sincronizado=True
        )
        
        # 2. Salva no banco usando seu serviço criar_conta
        criar_conta(nova_conta)

        # 3. Envia para o Google Agenda
        criar_lembrete_google(dados['descricao'], dados['data'], dados['valor'])
        
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Rota extra para listar as contas na sua tabela do site
@app.route('/api/contas/<int:usuario_id>', methods=['GET'])
def listar(usuario_id):
    try:
        contas = listar_contas_usuario(usuario_id)
        return jsonify([dict(row) for row in contas]), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)