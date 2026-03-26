from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_version   ="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key       =os.getenv("AZURE_OPENAI_KEY"),
)

def get_embedding(text: str):
    try:
        response = client.embeddings.create(
            model=os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print("ERROR EMBEDDING:", str(e))
        return None