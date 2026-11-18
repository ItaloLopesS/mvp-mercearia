from fastapi import FastAPI

app = FastAPI(title="Sistema de Controle de Estoque")


@app.get("/")
def inicio():
    return {
        "mensagem": "Sistema de Controle de Estoque funcionando!"
    }
