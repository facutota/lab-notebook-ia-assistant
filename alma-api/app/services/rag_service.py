import os
from openai import AzureOpenAI
from services.llm_service import call_gpt4o
from services.embeddings import get_embedding
from services.prompt_service import load_prompt
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

SYSTEM_PROMPT_RAG = load_prompt("system_rag.txt")

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
)

# 1. Buscar documentos
def search_documents(query: str):
    embedding = get_embedding(query)
    if embedding is None:
        return []
    try:
        results = search_client.search(
            search_text=None,
            vector=embedding,
            top=3,
            vector_fields="embedding"
        )

        docs = []
        for r in results:
            docs.append({
                "content": r.get("content", ""),
                "source": r.get("source", "unknown")
            })
        return docs
    except Exception as e:
        print("ERROR SEARCH:", str(e))
        return []


# 2. Construir contexto
def build_context(docs):
    context = ""
    for d in docs:
        context += f"\nFuente: {d['source']}\n{d['content']}\n"
    return context

# 🔹 3. Respuesta final
def rag_answer(query: str):
    try:
        docs = search_documents(query)
        if not docs:
            return "No hay información en la base de conocimiento"
        context = build_context(docs)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_RAG},
            {
                "role": "user",
                "content": f"Contexto:\n{context}\n\nPregunta:\n{query}"
            }
        ]

        return call_gpt4o(messages)

    except Exception as e:
        print("ERROR RAG:", str(e))
        return "Error en RAG"