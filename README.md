
# MVP - Controle de Estoque

Sistema de gerenciamento de estoque desenvolvido para uma pequena mercearia.

## Funcionalidades

- Cadastro de produtos.
- Consulta de produtos cadastrados.
- Registro de entrada de mercadorias.
- Registro de saída de mercadorias.
- Validação de estoque disponível.
- Armazenamento de dados com SQLite.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLite
- HTML
- CSS
- JavaScript
- Pytest

## Como executar

Instale as dependências:

    pip install -r requirements.txt

Inicie a aplicação:

    uvicorn main:app --reload

Acesse pelo navegador:

    http://127.0.0.1:8000

## Testes automatizados

Execute os testes com:

    python -m pytest -v

## Integração contínua

O GitHub Actions executa os testes automaticamente a cada atualização na branch principal e nos Pull Requests.

## Projeto acadêmico

Desenvolvido para a disciplina de Projeto de Software.
