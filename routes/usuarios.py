from fastapi import APIRouter, HTTPException
from database import conectar_db
from utils.security import gerar_hash

router = APIRouter()

@router.get("/usuarios")
def listar_usuarios():
    conexao = conectar_db()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, nome, email, foto_perfil, data_criacao FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conexao.close()
    return usuarios

@router.get("/usuarios/{id_usuario}")
def buscar_usuario(id_usuario: int):
    conexao = conectar_db()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, nome, email, foto_perfil, data_criacao FROM usuarios WHERE id_usuario=%s", (id_usuario,))
    usuario = cursor.fetchone()
    cursor.close()    
    conexao.close()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.post("/usuarios")
def criar_usuario(nome: str, email: str, senha: str):
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_usuario FROM usuarios where email=%s")
    if cursor.fetchone:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    senha_hash = gerar_hash(senha)
    sql = "INSERT INTO usuarios (nome, email, senha_hash) VALUES (%s, %s, %s)"
    valores = (nome, email, senha_hash)
    cursor.execute(sql, valores)    
    conexao.commit()
    cursor.close()
    conexao.close()
    return {"mensagem": "Usuário criado com sucesso"}

@router.put("/usuarios/{id_usuario}")
def atualizar_usuario(id_usuario: int, nome: str, email: str):
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute("UPDATE usuarios SET nome=%s, email=%s WHERE id_usuario=%s",(nome, email, id_usuario))
    conexao.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    cursor.close()
    conexao.close()
    return {"mensagem": "Usuário atualizado"}

@router.delete("/usuarios/{id_usuario}")
def deletar_usuario(id_usuario: int):
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_usuario,))
    conexao.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    cursor.close()
    conexao.close()
    return {"mensagem": "Usuário deletado"}