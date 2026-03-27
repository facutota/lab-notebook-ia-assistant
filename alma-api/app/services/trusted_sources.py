import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "trusted_sources.json"

def get_trusted_sources(domain: str) -> list:
    try:
        if not DATA_PATH.exists():
            return []

        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

        # dominio específico
        sources = data.get(domain, [])

        # fallback general: juntar todas las urls únicas
        if domain == "general" or not sources:
            all_sources = []
            for k, v in data.items():
                if isinstance(v, list):
                    all_sources.extend(v)
            return sorted(list(set(all_sources)))

        return sources

    except Exception as e:
        print("ERROR TRUSTED SOURCES:", str(e))
        return []