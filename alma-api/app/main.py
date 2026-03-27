import os
from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from services.llm_service import call_nano
from services.router import route
from services.rag_service import rag_answer
from services.multimodal_service import multimodal_answer
from services.content_safety_service import check_text_safety

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins    =["*"],
    allow_credentials=True,
    allow_methods    =["*"],
    allow_headers    =["*"],
)

def load_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

SYSTEM_PROMPT_NANO = load_prompt("prompts/system_assistant.txt")

class ChatRequest(BaseModel):
    message: str
    files  : list = []

@app.get("/health")
def health():
    return {"status": "ok"}

def rag_fallback(query):
    return f"[RAG EN CONSTRUCCION] Consulta recibida: {query}"

def multimodal_fallback(query):
    return f"[MULTIMODAL REQUIERE INTERVENCION DEL SUPERVISOR] Consulta recibida: {query}"

@app.post("/chat_upload")
async def chat_upload(
    message: str = Form(...),
    persistence: str = Form("temporary"),
    files: Optional[List[UploadFile]] = File(None)
):
    safety = check_text_safety(message)

    if not safety["allowed"]:
        return {
            "reply"  : "No puedo ayudar con esa solicitud porque puede involucrar contenido sensible o peligroso.",
            "blocked": True,
            "safety" : safety
        }
        
    try:
        files = files or []
        reply = await multimodal_answer(message, files, persistence)
        return {"reply": reply}
    except Exception as e:
        print("ERROR UPLOAD:", str(e))
        return {"error": str(e), "type": "system_error"}

@app.post("/chat")
async def chat(req: ChatRequest):
    safety = check_text_safety(req.message)

    if not safety["allowed"]:
        return {
            "reply": "No puedo ayudar con esa solicitud porque puede involucrar contenido sensible o peligroso.",
            "blocked": True,
            "safety": safety
        }
        
    try:
        route_type = route(req.message, req.files)
        print("ROUTE:", route_type)

        if route_type == "simple":
            reply = call_nano([
                {"role": "system", "content": SYSTEM_PROMPT_NANO},
                {"role": "user"  , "content"  : req.message}
            ])

        elif route_type == "rag":
            reply = rag_answer(req.message)

        elif route_type == "multimodal":
            reply = "Este endpoint no soporta archivos. Usa /chat_upload."

        else:
            reply = "[ROUTE DESCONOCIDA]"

        return {"reply": reply}

    except Exception as e:
        print("ERROR   :", str(e))
        return {"error": str(e), "type": "system_error"}