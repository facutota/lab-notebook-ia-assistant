import os

def load_prompt(filename: str) -> str:
    base_path = os.path.dirname(os.path.dirname(__file__))  # app/
    path = os.path.join(base_path, "prompts", filename)

    with open(path, "r", encoding="utf-8") as f:
        return f.read()