import json
import os
import uuid
from typing import List, Dict

DATA_FILE = "data/eventos.json"
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

def load_events() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            eventos = json.load(f)
            # FORÇA ID em todos os eventos carregados
            for ev in eventos:
                if "id" not in ev or not ev["id"] or ev["id"] in ("", "None", None):
                    ev["id"] = str(uuid.uuid4())
            return eventos
    except Exception as e:
        print(f"Erro ao carregar eventos: {e}")
        return []

def save_events(eventos: List[Dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(eventos, f, ensure_ascii=False, indent=4)