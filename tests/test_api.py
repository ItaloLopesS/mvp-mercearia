
from fastapi.testclient import TestClient
from main import app
import database
import pytest


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    banco_teste = tmp_path / "teste.db"
    monkeypatch.setattr(database, "DB_PATH", str(banco_teste))

    with TestClient(app) as client:
        yield client


def test_cadastrar_produto(cliente):
    resposta = cliente.post("/produtos", json={
        "nome": "Arroz",
        "quantidade": 10,
        "preco": 25.50
    })

    assert resposta.status_code == 200

    produtos = cliente.get("/produtos").json()

    assert len(produtos) == 1
    assert produtos[0]["nome"] == "Arroz"


def test_entrada_estoque(cliente):
    cliente.post("/produtos", json={
        "nome": "Feijão",
        "quantidade": 10,
        "preco": 8.00
    })

    resposta = cliente.post("/estoque/entrada", json={
        "produto_id": 1,
        "quantidade": 5
    })

    assert resposta.status_code == 200

    produtos = cliente.get("/produtos").json()
    assert produtos[0]["quantidade"] == 15


def test_saida_estoque(cliente):
    cliente.post("/produtos", json={
        "nome": "Açúcar",
        "quantidade": 10,
        "preco": 5.00
    })

    resposta = cliente.post("/estoque/saida", json={
        "produto_id": 1,
        "quantidade": 3
    })

    assert resposta.status_code == 200

    produtos = cliente.get("/produtos").json()
    assert produtos[0]["quantidade"] == 7


def test_saida_com_estoque_insuficiente(cliente):
    cliente.post("/produtos", json={
        "nome": "Macarrão",
        "quantidade": 5,
        "preco": 4.00
    })

    resposta = cliente.post("/estoque/saida", json={
        "produto_id": 1,
        "quantidade": 10
    })

    assert resposta.status_code == 400
