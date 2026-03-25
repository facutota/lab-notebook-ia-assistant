from openai import AzureOpenAI
import os
from dotenv import load_dotenv

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
            messages=messages,
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