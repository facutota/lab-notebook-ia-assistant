import os
from services.llm_service import call_gpt4o
from services.embeddings import get_embedding
from services.prompt_service import load_prompt
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from services.trusted_sources import get_trusted_sources

SYSTEM_PROMPT_RAG = load_prompt("system_rag.txt")

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
)

# RAG helper dominios
def infer_domain(doc_id: str) -> str:
    if not doc_id:
        return "unknown"

    s = doc_id.lower()

    if "/docs/ethics/" in s:
        return "ethics"
    if "/docs/protocols/" in s:
        return "protocols"
    if "/docs/biologia/" in s:
        return "biologia"

    return "unknown"


# 1. Buscar documentos
def search_documents(query: str):
    embedding = get_embedding(query)
    if embedding is None:
        return []

    try:
        results = search_client.search(
            search_text=query,
            vector_queries=[{
                "kind": "vector",
                "vector": embedding,
                "k": 8,
                "fields": "embedding"
            }],
            top=8,
            select=["id", "content", "source", "title"]
        )

        docs = []
        for r in results:
            doc_id = r.get("id", "")
            domain = infer_domain(doc_id)

            # Si source viene null, usamos doc_id como fuente (porque contiene el path del blob)
            source = r.get("source")
            if not source:
                source = doc_id

            docs.append({
                "id": doc_id,
                "domain": domain,
                "title": r.get("title", "unknown"),
                "source": source,
                "content": r.get("content", "")
            })

        return docs

    except Exception as e:
        print("ERROR SEARCH:", str(e))
        return []


# 2. Construir contexto
def build_context(docs):
    context = ""
    for d in docs:
        context += (
            f"\n[Dominio: {d['domain']}]\n"
            f"Titulo: {d['title']}\n"
            f"Fuente: {d['source']}\n"
            f"{d['content']}\n"
        )
    return context


# 3. Elegir dominio dominante (para trusted sources)
def get_main_domain(docs):
    counts = {}
    for d in docs:
        dom = d.get("domain", "unknown")
        counts[dom] = counts.get(dom, 0) + 1

    if not counts:
        return "general"

    # dominio con más ocurrencias
    return max(counts, key=counts.get)


# 4. Respuesta final
def rag_answer(query: str):
    try:
        docs = search_documents(query)

        if not docs:
            sources = get_trusted_sources("general")
            if sources:
                return (
                    "No encontré información en la base de conocimiento interna.\n\n"
                    "Fuentes oficiales sugeridas:\n" +
                    "\n".join(sources)
                )
            return "No hay información en la base de conocimiento"

        main_domain = get_main_domain(docs)
        context = build_context(docs)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_RAG},
            {
                "role": "user",
                "content": (
                    f"Dominio principal detectado: {main_domain}\n\n"
                    f"Contexto:\n{context}\n\n"
                    f"Pregunta:\n{query}\n\n"
                    "Instrucción: Responde SOLO usando el contexto entregado. "
                    "Si no hay evidencia suficiente en el contexto, dilo explícitamente."
                )
            }
        ]

        return call_gpt4o(messages)

    except Exception as e:
        print("ERROR RAG:", str(e))
        return "Error en RAG"