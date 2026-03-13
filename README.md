# fastApi-tcc

API REST feita em Python usando FastAPI.

## Tecnologias
- Python
- FastAPI
- MySQL
- Uvicorn
- bcrypt

## Funcionalidades
- CRUD de usuários
- CRUD de grupos de viagem
- Busca de grupos por nome
- Login com senha criptografada
- Integração com MySQL
- Autenticação de usuário

## Como executar

1. Baixe o repositório

https://github.com/gabrieljurgensen-dev/fastApi-tcc.git

2. Instale as dependências

pip install -r requirements.txt

3. Execute a aplicação

uvicorn main:app --reload

4. Acesse a documentação automática da API

http://127.0.0.1:8000/docs

### Usuários
POST /usuarios - Criar usuário  
GET /usuarios - Listar usuários  
PUT /usuarios/{id_usuario} - Atualizar usuário  
DELETE /usuarios/{id_usuario} - Deletar usuário  

### Grupos de viagem
POST /grupos - Criar grupo  
GET /grupos - Listar grupos  
GET /grupos/{id_grupo} - Buscar grupo por ID  
PUT /grupos/{id_grupo} - Atualizar grupo  
DELETE /grupos/{id_grupo} - Deletar grupo
