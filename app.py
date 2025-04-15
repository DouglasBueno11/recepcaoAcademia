from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Carregar credenciais do Firebase a partir de variáveis de ambiente
load_dotenv()
FBKEY = json.loads(os.getenv('CONFIG_FIREBASE'))
cred = credentials.Certificate(FBKEY)
firebase_admin.initialize_app(cred)

# Inicializar o cliente Firestore
db = firestore.client()

# Rota principal
@app.route('/')
def index():
    return 'Sistema da Academia ON!'

# Verificar status do aluno pelo CPF (para catraca)
@app.route('/alunos/<cpf>', methods=['GET'])
def verificar_acesso(cpf):
    query = db.collection('alunos').where('cpf', '==', cpf).limit(1)
    results = query.get()
    
    if not results:
        return jsonify({'mensagem': 'CPF não cadastrado'}), 404
    
    aluno_data = results[0].to_dict()
    
    if aluno_data['status']:
        return jsonify({'status': True, 'mensagem': 'Acesso liberado'}), 200
    else:
        return jsonify({'status': False, 'mensagem': 'Procure a secretaria da academia'}), 403

# Listar todos os alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = []
    docs = db.collection('alunos').stream()
    
    for doc in docs:
        aluno_data = doc.to_dict()
        aluno_data['id'] = doc.id
        alunos.append(aluno_data)
    
    return jsonify(alunos), 200

# Obter dados completos de um aluno (para admin)
@app.route('/alunos/<cpf>/dados', methods=['GET'])
def obter_dados_aluno(cpf):
    query = db.collection('alunos').where('cpf', '==', cpf).limit(1)
    results = query.get()
    
    if not results:
        return jsonify({'mensagem': 'Aluno não encontrado'}), 404
    
    aluno_data = results[0].to_dict()
    aluno_data['id'] = results[0].id
    return jsonify(aluno_data), 200

# Cadastrar novo aluno
@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    dados = request.json
    required_fields = ['nome', 'cpf', 'status']
    
    if not all(field in dados for field in required_fields):
        return jsonify({'mensagem': 'Campos obrigatórios: nome, cpf, status'}), 400
    
    if not isinstance(dados['status'], bool):
        return jsonify({'mensagem': 'Status deve ser booleano'}), 400
    
    # Verificar se o CPF já existe
    query = db.collection('alunos').where('cpf', '==', dados['cpf']).limit(1)
    if query.get():
        return jsonify({'mensagem': 'CPF já cadastrado'}), 409
    
    # Gerar ID automático e salvar o documento
    doc_ref = db.collection('alunos').doc()
    doc_ref.set({
        'nome': dados['nome'],
        'cpf': dados['cpf'],
        'status': dados['status']
    })
    
    return jsonify({'mensagem': 'Aluno cadastrado com sucesso', 'id': doc_ref.id}), 201

# Atualizar aluno
@app.route('/alunos/<cpf>', methods=['PUT'])
def atualizar_aluno(cpf):
    dados = request.json
    required_fields = ['nome', 'status']
    
    if not all(field in dados for field in required_fields):
        return jsonify({'mensagem': 'Campos obrigatórios: nome, status'}), 400
    
    if not isinstance(dados['status'], bool):
        return jsonify({'mensagem': 'Status deve ser booleano'}), 400
    
    query = db.collection('alunos').where('cpf', '==', cpf).limit(1)
    results = query.get()
    
    if not results:
        return jsonify({'mensagem': 'Aluno não encontrado'}), 404
    
    doc_ref = results[0].reference
    doc_ref.update({
        'nome': dados['nome'],
        'status': dados['status']
    })
    
    return jsonify({'mensagem': 'Aluno atualizado com sucesso'}), 200

# Excluir aluno
@app.route('/alunos/<cpf>', methods=['DELETE'])
def excluir_aluno(cpf):
    query = db.collection('alunos').where('cpf', '==', cpf).limit(1)
    results = query.get()
    
    if not results:
        return jsonify({'mensagem': 'Aluno não encontrado'}), 404
    
    doc_ref = results[0].reference
    doc_ref.delete()
    return jsonify({'mensagem': 'Aluno excluído com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)