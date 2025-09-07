from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json, os

ARQUIVO_MUNDO = "world_root.json"

app = FastAPI()

def carregar_mundo():
    with open(ARQUIVO_MUNDO, encoding="utf-8") as f:
        return json.load(f)

def salvar_mundo(mundo):
    with open(ARQUIVO_MUNDO, "w", encoding="utf-8") as f:
        json.dump(mundo, f, ensure_ascii=False, indent=2)

@app.get("/mundo")
def get_mundo():
    return carregar_mundo()

class AdminAction(BaseModel):
    usuario: str
    comando: str

@app.post("/admin")
def admin_action(action: AdminAction):
    mundo = carregar_mundo()
    user = next((u for u in mundo["usuarios"] if u["login"] == action.usuario), None)
    if not user or user.get("permissao") != "odin":
        return JSONResponse({"erro": "Permissão negada."}, status_code=403)
    if action.comando.startswith("adicionar lei"):
        try:
            partes = action.comando.split(":", 1)
            distrito_nome, lei = partes[1].split("|")
            distrito = next(d for d in mundo["planeta"]["distritos"] if d["nome"] == distrito_nome.strip())
            mundo["numeradores"]["lei"] += 1
            distrito["leis"].append({"id": mundo["numeradores"]["lei"], "descricao": lei.strip()})
            user["historico_acoes"].append({"acao": action.comando})
            salvar_mundo(mundo)
            return {"msg": "Lei adicionada!"}
        except Exception as e:
            return JSONResponse({"erro": "Falha ao adicionar lei: "+str(e)}, status_code=400)
    return {"msg": "Comando reconhecido, mas não implementado ainda."}

@app.post("/chat")
def post_chat(msg: dict):
    mundo = carregar_mundo()
    mundo["numeradores"]["chat_id_atual"] += 1
    chat_id = mundo["numeradores"]["chat_id_atual"]
    registro = {
        "id": chat_id,
        "usuario": msg.get("usuario"),
        "mensagem": msg.get("mensagem"),
        "resposta": msg.get("resposta", ""),
    }
    mundo.setdefault("chats", []).append(registro)
    salvar_mundo(mundo)
    return {"msg": "Registro salvo.", "chat_id": chat_id}