from app.services.prompt_service import load_prompt
import openai
from dotenv import load_dotenv
import os

load_dotenv()

SYSTEM_PROMPT_GPT4O    = load_prompt("system_prompt_4.txt")
SYSTEM_PROMPT_ROUTER   = load_prompt("system_router.txt")
SYSTEM_PROMPT_ASSISTANT= load_prompt("system_assistant.txt")

client = openai.AzureOpenAI(
    api_version    = os.getenv("AZURE_API_VERSION"),
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key        = os.getenv("AZURE_OPENAI_KEY"),
)

# GPT-4o (RAG / razonamiento)
def call_gpt4o(messages):
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT_GPT4O"),
            messages=messages,
            max_tokens=1500
        )
        return response.choices[0].message.content

    except Exception as e:
        print("ERROR GPT4O:", str(e))
        return "Error en GPT-4o"


# Router (direccionamiento/respuestas simples)
def call_nano(messages: str) -> str:
    system_prompt_ = load_prompt("system_assistant.txt")
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT_NANO"),  # gpt-4.1-router
            messages=messages,
            max_tokens=300
        )
        return response.choices[0].message.content

    except Exception as e:
        print("ERROR NANO:", str(e))
        return "Error en modelo router"