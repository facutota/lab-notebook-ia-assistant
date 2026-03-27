import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "trusted_sources.json"

def get_trusted_sources(domain: str) -> list:
    if not DATA_PATH.exists():
        return []
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return data.get(domain, [])