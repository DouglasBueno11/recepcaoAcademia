from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

FBKEY = json.loads(os.getenv('CONFIG_FIREBASE'))

cred = credentials.Certificate(FBKEY)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Rota principal
@app.route('/')
def index():
    return 'Sistema da Academia ON!'

# Verificar status do aluno pelo CPF (Para catraca)
@app.route('/alunos/<cpf>', methods=['GET'])
def verificar_acesso(cpf):
    aluno_ref = db.collection('alunos').document(cpf)
    aluno = aluno_ref.get()
    
    if not aluno.exists:
        return jsonify({'mensagem': 'CPF não cadastrado'}), 404
    
    aluno_data = aluno.to_dict()
    
    if aluno_data['status'] == 'ativo':
        return jsonify({'status': 'ativo', 'mensagem': 'Acesso liberado'}), 200
    else:
        return jsonify({'status': 'bloqueado', 'mensagem': 'Procure a secretaria da academia'}), 403

# Listar todos os alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = []
    docs = db.collection('alunos').stream()
    
    for doc in docs:
        alunos.append(doc.to_dict())
    
    return jsonify(alunos), 200

# Cadastrar novo aluno
@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    dados = request.json
    required_fields = ['nome', 'cpf', 'status']
    
    if not all(field in dados for field in required_fields):
        return jsonify({'mensagem': 'Campos obrigatórios: nome, cpf, status'}), 400
    
    if dados['status'] not in ['ativo', 'bloqueado']:
        return jsonify({'mensagem': 'Status inválido (use "ativo" ou "bloqueado")'}), 400
    
    cpf = dados['cpf']
    if db.collection('alunos').document(cpf).get().exists:
        return jsonify({'mensagem': 'CPF já cadastrado'}), 409
        
    db.collection('alunos').document(cpf).set({
        'nome': dados['nome'],
        'cpf': cpf,
        'status': dados['status']
    })
    
    return jsonify({'mensagem': 'Aluno cadastrado com sucesso'}), 201

# Atualizar aluno
@app.route('/alunos/<cpf>', methods=['PUT'])
def atualizar_aluno(cpf):
    dados = request.json
    required_fields = ['nome', 'status']
    
    if not all(field in dados for field in required_fields):
        return jsonify({'mensagem': 'Campos obrigatórios: nome, status'}), 400
    
    if dados['status'] not in ['ativo', 'bloqueado']:
        return jsonify({'mensagem': 'Status inválido (use "ativo" ou "bloqueado")'}), 400
    
    aluno_ref = db.collection('alunos').document(cpf)
    if not aluno_ref.get().exists:
        return jsonify({'mensagem': 'Aluno não encontrado'}), 404
    
    aluno_ref.update({
        'nome': dados['nome'],
        'status': dados['status']
    })
    
    return jsonify({'mensagem': 'Aluno atualizado com sucesso'}), 200

# Excluir aluno
@app.route('/alunos/<cpf>', methods=['DELETE'])
def excluir_aluno(cpf):
    aluno_ref = db.collection('alunos').document(cpf)
    if not aluno_ref.get().exists:
        return jsonify({'mensagem': 'Aluno não encontrado'}), 404
    
    aluno_ref.delete()
    return jsonify({'mensagem': 'Aluno excluído com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)