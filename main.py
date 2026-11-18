from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Sistema de Controle de Estoque")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def inicio():
    return FileResponse("index.html")
