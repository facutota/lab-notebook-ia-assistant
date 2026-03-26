import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
#from router import route
#from llm_service import call_gpt4o, call_nano
from services.llm_service import call_gpt4o, call_nano
from services.router import route

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins    =["*"],
    allow_credentials=True,
    allow_methods    =["*"],
    allow_headers    =["*"],
)

SYSTEM_PROMPT_4    = os.getenv("SYSTEM_PROMPT_4")
SYSTEM_PROMPT_NANO = os.getenv("SYSTEM_PROMPT_NANO")


class ChatRequest(BaseModel):
    message: str
    files  : list[str] = []


@app.get("/health")
def health():
    return {"status": "ok"}

def rag_fallback(query):
    return f"[RAG NO IMPLEMENTADO] Consulta recibida: {query}"

def multimodal_fallback():
    return "[MULTIMODAL NO IMPLEMENTADO]"

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        route_type = route(req.message, req.files)
        print("ROUTE:", route_type)

        if route_type == "simple":
            reply = call_nano([
                {"role": "system", "content": SYSTEM_PROMPT_NANO},
                {"role": "user", "content"  : req.message}
            ])

        elif route_type == "rag":
            reply = rag_fallback(req.message)

        elif route_type == "multimodal":
            reply = multimodal_fallback()

        else:
            reply = "[ROUTE DESCONOCIDA]"

        return {"reply": reply}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e), "type": "system_error"}