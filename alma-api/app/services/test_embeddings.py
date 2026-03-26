from services.embeddings import get_embedding
result = get_embedding("hola mundo")

if result:
    print("OK, dimensiones:", len(result))
else:
    print("Error en embeddings")