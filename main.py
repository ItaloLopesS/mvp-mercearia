from fastapi import FastAPI, HTTPException
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


class Movimentacao(BaseModel):
    produto_id: int
    quantidade: int


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
    if produto.quantidade < 0 or produto.preco < 0:
        raise HTTPException(400, "Valores inválidos.")

    conexao = conectar()

    conexao.execute(
        """INSERT INTO produtos (nome, quantidade, preco)
        VALUES (?, ?, ?)""",
        (produto.nome, produto.quantidade, produto.preco)
    )

    conexao.commit()
    conexao.close()

    return {"mensagem": "Produto cadastrado com sucesso!"}


@app.post("/estoque/entrada")
def entrada_estoque(movimentacao: Movimentacao):
    if movimentacao.quantidade <= 0:
        raise HTTPException(400, "Quantidade inválida.")

    conexao = conectar()

    produto = conexao.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (movimentacao.produto_id,)
    ).fetchone()

    if produto is None:
        conexao.close()
        raise HTTPException(404, "Produto não encontrado.")

    conexao.execute(
        "UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?",
        (movimentacao.quantidade, movimentacao.produto_id)
    )

    conexao.commit()
    conexao.close()

    return {"mensagem": "Entrada registrada com sucesso!"}


@app.post("/estoque/saida")
def saida_estoque(movimentacao: Movimentacao):
    if movimentacao.quantidade <= 0:
        raise HTTPException(400, "Quantidade inválida.")

    conexao = conectar()

    produto = conexao.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (movimentacao.produto_id,)
    ).fetchone()

    if produto is None:
        conexao.close()
        raise HTTPException(404, "Produto não encontrado.")

    if produto["quantidade"] < movimentacao.quantidade:
        conexao.close()
        raise HTTPException(400, "Estoque insuficiente.")

    conexao.execute(
        "UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?",
        (movimentacao.quantidade, movimentacao.produto_id)
    )

    conexao.commit()
    conexao.close()

    return {"mensagem": "Saída registrada com sucesso!"}
