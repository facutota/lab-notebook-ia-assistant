from app.services.prompt_service import load_prompt
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

SYSTEM_PROMPT_RAG = load_prompt("system_rag.txt")