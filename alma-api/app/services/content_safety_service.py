import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential


client = ContentSafetyClient(
    endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_CONTENT_SAFETY_KEY"))
)


def check_text_safety(text: str) -> dict:
    """
    Retorna dict con:
    {
      "allowed" : bool,
      "severity": { "Hate": int, "SelfHarm": int, "Sexual": int, "Violence": int }
    }
    """
    try:
        if not text or len(text.strip()) == 0:
            return {"allowed": True, "severity": {}}

        request = AnalyzeTextOptions(text=text)
        result = client.analyze_text(request)

        severity = {}
        for item in result.categories_analysis:
            severity[item.category] = item.severity

        # Política MVP: bloquear si alguna categoría >= 3
        blocked = any(v >= 3 for v in severity.values())

        return {
            "allowed" : not blocked,
            "severity": severity
        }

    except Exception as e:
        print("ERROR CONTENT SAFETY:", str(e))
        # Dejamos un fallback seguro: Permite, si falla safety (para no matar el sistema)
        return {"allowed": True, "severity": {}, "error": str(e)}