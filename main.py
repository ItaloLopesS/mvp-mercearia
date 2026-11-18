from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from database import conectar, criar_tabela

app = FastAPI(title="Sistema de Controle de Estoque")

app.mount("/static", StaticFiles(directory="static"), name="static")


class Produto(BaseModel):
    nome: str
    quantidade: int
    preco: float


@app.on_event("startup")
def iniciar():
    criar_tabela()


@app.get("/")
def inicio():
    return FileResponse("index.html")


@app.get("/produtos")
def listar_produtos():
    conexao = conectar()
    produtos = conexao.execute(
        "SELECT * FROM produtos"
    ).fetchall()
    conexao.close()

    return [dict(produto) for produto in produtos]


@app.post("/produtos")
def cadastrar_produto(produto: Produto):
    conexao = conectar()

    conexao.execute(
        "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
        (produto.nome, produto.quantidade, produto.preco)
    )

    conexao.commit()
    conexao.close()

    return {"mensagem": "Produto cadastrado com sucesso!"}
