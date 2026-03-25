from app.services.prompt_service import load_prompt
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

SYSTEM_PROMPT_GPT4O  = load_prompt("system_prompt_4.txt")
SYSTEM_PROMPT_ROUTER = load_prompt("system_router.txt")

load_dotenv()

client = AzureOpenAI(
    api_version   =os.getenv("AZURE_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key       =os.getenv("AZURE_OPENAI_KEY"),
)

def call_gpt4o(messages):
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT_GPT4O"),
            messages=[
            {"role": "system", "content": SYSTEM_PROMPT_GPT4O},
            {"role": "user", "content": user_message}
        ],
            max_completion_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        print("ERROR GPT4O:", str(e))
        return "Error en GPT-4o"

def call_nano(messages):
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT_NANO"),
            messages=messages,
            max_completion_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        print("ERROR NANO:", str(e))
        return "Error en GPT-5-nano"