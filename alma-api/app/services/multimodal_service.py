import base64
from typing import List
from fastapi import UploadFile
from services.llm_service import call_gpt4o
from pypdf import PdfReader
import io


def encode_file(file: UploadFile) -> str:
    return base64.b64encode(file.file.read()).decode("utf-8")


def extract_pdf_text(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    return text.strip()


async def multimodal_answer(query: str, files: List[UploadFile], persistence: str) -> str:
    content = []

    if query:
        content.append({"type": "text", "text": query})

    extracted_text = ""

    for file in files:
        filename = file.filename.lower()

        if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
            base64_image = encode_file(file)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                }
            })

        elif filename.endswith(".pdf"):
            file_bytes = await file.read()
            pdf_text = extract_pdf_text(file_bytes)
            if pdf_text:
                extracted_text += f"\n\n[PDF: {file.filename}]\n{pdf_text[:12000]}"

        elif filename.endswith(".txt"):
            file_bytes = await file.read()
            extracted_text += f"\n\n[TXT: {file.filename}]\n{file_bytes.decode('utf-8', errors='ignore')[:12000]}"

    if extracted_text:
        content.append({"type": "text", "text": f"Contenido adjunto extraído:\n{extracted_text}"})

    messages = [
        {"role": "system", "content": "Eres ALMA, un asistente científico. Analiza los adjuntos y responde con rigor."},
        {"role": "user", "content": content}
    ]

    return call_gpt4o(messages)