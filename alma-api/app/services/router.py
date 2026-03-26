def route(query: str, files: list):
    query_lower = query.lower()

    # 1. Si hay archivos
    if files:
        file_types = [f.lower() for f in files]

        if any(ft.endswith((".pdf", ".csv", ".docx", ".xlsx", ".txt")) for ft in file_types):
            return "rag"

        if any(ft.endswith((".png", ".jpg", ".jpeg", ".mp3", ".wav")) for ft in file_types):
            return "multimodal"

    # 2. Keywords de RAG
    keywords = ["protocolo", "protocol", "norma", "ética", "manual", "regulación", "experimento"]

    if any(k in query_lower for k in keywords):
        return "rag"

    # 3. Default o Fallback
    return "simple"
