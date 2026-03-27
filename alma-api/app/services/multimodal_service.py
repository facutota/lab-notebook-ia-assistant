import os
import io
import base64
import uuid
from datetime import datetime, timezone
from typing import List
from fastapi import UploadFile
from pypdf import PdfReader
from azure.storage.blob.aio import BlobServiceClient
from services.llm_service import call_gpt4o

BLOB_CONTAINER = "contenedor-docs-alma"

def extract_pdf_text(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    return text.strip()

def encode_image_base64(file_bytes: bytes) -> str:
    return base64.b64encode(file_bytes).decode("utf-8")

async def upload_to_blob(file_bytes: bytes, filename: str, persistence: str) -> str:
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        raise Exception("AZURE_STORAGE_CONNECTION_STRING no está configurado en .env")

    blob_service = BlobServiceClient.from_connection_string(conn_str)

    folder    = "uploads_temporales" if persistence == "temporary" else "uploads_persistentes"
    safe_name = filename.replace(" ", "_")
    blob_name = f"{folder}/{datetime.now(timezone.utc).strftime('%Y%m%d')}/{uuid.uuid4()}_{safe_name}"

    blob_client = blob_service.get_blob_client(container=BLOB_CONTAINER, blob=blob_name)
    await blob_client.upload_blob(file_bytes, overwrite=True)

    return blob_name

async def multimodal_answer(query: str, files: List[UploadFile], persistence: str) -> str:
    content = []

    if query:
        content.append({"type": "text", "text": query})

    extracted_text = ""
    stored_paths   = []

    for file in files:
        filename   = file.filename or "unknown"
        file_bytes = await file.read()

        # Guardar en blob (siempre)
        try:
            blob_path = await upload_to_blob(file_bytes, filename, persistence)
            stored_paths.append(blob_path)
        except Exception as e:
            stored_paths.append(f"[ERROR SUBIENDO {filename}: {str(e)}]")

        lower = filename.lower()

        # Imagen
        if lower.endswith((".png", ".jpg", ".jpeg", ".webp")):
            b64 = encode_image_base64(file_bytes)
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}"}
            })

        # PDF
        elif lower.endswith(".pdf"):
            text = extract_pdf_text(file_bytes)
            if text:
                extracted_text += f"\n\n[PDF: {filename}]\n{text[:12000]}"

        # TXT
        elif lower.endswith(".txt"):
            extracted_text += f"\n\n[TXT: {filename}]\n{file_bytes.decode('utf-8', errors='ignore')[:12000]}"

    if stored_paths:
        extracted_text += "\n\nArchivos almacenados en Blob:\n" + "\n".join(stored_paths)

    if extracted_text.strip():
        content.append({"type": "text", "text": f"Contenido extraído:\n{extracted_text}"})

    messages = [
        {
            "role": "system",
            "content": (
                "Eres ALMA, un asistente científico. "
                "Analiza los adjuntos y responde con rigor. "
                "Si falta información, dilo explícitamente."
            )
        },
        {"role": "user", "content": content}
    ]

    #return call_gpt4o(messages)
    reply = call_gpt4o(messages)

    # Guardar el insight si es persistente
    if persistence == "persistent":
        try:
            insights_filename = f"insights_{uuid.uuid4()}.txt"
            await upload_to_blob(reply.encode("utf-8"), insights_filename, persistence)
            print("INSIGHTS GUARDADOS:", insights_filename)
        except Exception as e:
            print("ERROR GUARDANDO INSIGHTS:", str(e))

    return reply