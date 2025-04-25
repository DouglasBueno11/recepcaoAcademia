# 💪 Sistema de Gerenciamento de Alunos - Academia ON

Este é um sistema de gerenciamento de alunos desenvolvido com **Flask** e **Firebase Firestore**, projetado para academias que desejam controlar o acesso de seus alunos por meio do CPF, além de realizar cadastros, atualizações e exclusões de dados dos mesmos.

---

## 🚀 Funcionalidades

- ✅ Verificação de status de alunos por CPF (integração com catraca)
- 📋 Listagem de todos os alunos
- 🔍 Consulta de aluno por ID
- ➕ Cadastro de novos alunos
- ✏️ Atualização de dados do aluno
- 🗑️ Exclusão de alunos

---

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Firebase Firestore](https://firebase.google.com/products/firestore)
- [Flask-CORS](https://flask-cors.readthedocs.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## ⚙️ Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- Firebase configurado com uma coleção chamada `alunos` e um documento `controle_id` com o campo `id`.

### 1. Clonar o repositório

```bash
git clone https://github.com/DouglasBueno11/recepcaoAcademia.git
cd nome-do-repositorio
```

### 2. Criar e configurar o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
CONFIG_FIREBASE='{"type": "...", "project_id": "...", "private_key_id": "...", ... }'
```

> Use as credenciais do Firebase exportadas no formato JSON. Copie e cole tudo dentro da variável `CONFIG_FIREBASE` (com aspas simples externas).

---

## 🧪 Como usar

### Iniciar o servidor

```bash
python app.py
```

O servidor estará disponível em: [http://localhost:5000](http://localhost:5000)

---

## 📡 Rotas da API

| Método | Rota                      | Descrição                                  |
|--------|---------------------------|--------------------------------------------|
| GET    | `/`                       | Rota de teste da API                       |
| GET    | `/alunos/<cpf>`           | Verifica se o aluno tem acesso liberado    |
| GET    | `/alunos`                 | Lista todos os alunos                      |
| GET    | `/alunos/id/<id>`         | Retorna dados completos do aluno por ID    |
| POST   | `/alunos`                 | Cadastra um novo aluno                     |
| PUT    | `/alunos/<id>`            | Atualiza dados de um aluno                 |
| DELETE | `/alunos/<id>`            | Exclui um aluno                            |

---

## 📂 Estrutura esperada no Firestore

### Coleção: `alunos`
```json
{
  "id": 1,
  "nome": "João da Silva",
  "cpf": "12345678900",
  "status": true
}
```

### Documento: `controle_id` (na coleção `controle_id`)
```json
{
  "id": 1
}
```

## 💻✨ Acesse o Front-End
- Administrador:
  - GitHub: https://github.com/gabrielcamargogsilva/Projeto-Academia-Admin.git
  - Vercel: https://projeto-academia-admin-liart.vercel.app/

- Catraca:
  - GitHub: https://github.com/gabrielcamargogsilva/Projeto-Academia-Cliente.git
  - Vercel: https://projeto-academia-cliente.vercel.app/

## 🧑‍💻 Autor

Desenvolvido por: 
- [Douglas Willian Bueno Sobrinho](https://github.com/DouglasBueno11)
  
  📧 Email: 
    - douglas.bueno.senai@gmail.com
    - douglas.w.sobrinho@aluno.senai.br
    - douglaswillianbueno.com@gmail.com

- [Gabriel Gonsalves Camargo Silva](https://github.com/gabrielcamargogsilva)
  
  📧 Email: 
    - gabrielcamargogsilva@gmail.com
    - gabriel.cgsilva.senai@gmail.com

---