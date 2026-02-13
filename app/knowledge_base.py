from __future__ import annotations

import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "diseases.json"


def load_knowledge_base() -> dict:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_categories(data: dict) -> list[str]:
    return sorted(data.keys())


def retrieve_diseases(data: dict, category: str, question: str, animal_name: str | None = None) -> list[dict]:
    category_data = data.get(category, [])
    if not category_data:
        return []

    text = question.lower()
    animal = (animal_name or "").lower().strip()

    scored: list[tuple[int, dict]] = []
    for disease in category_data:
        score = 0

        name = disease.get("name", "").lower()
        if name and name in text:
            score += 4

        for sym in disease.get("symptoms", []):
            if sym.lower() in text:
                score += 2

        for sp in disease.get("species", []):
            sp_lower = sp.lower()
            if sp_lower and sp_lower in text:
                score += 2
            if animal and animal == sp_lower:
                score += 3

        if score > 0:
            scored.append((score, disease))

    if scored:
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:4]]

    # Fallback: return top few diseases in that category when no strong keyword match exists.
    return category_data[:3]
