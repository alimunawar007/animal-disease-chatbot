from __future__ import annotations

from typing import Iterable


SYSTEM_PROMPT_TEMPLATE = """
You are VetCare Assistant, a careful veterinary disease support chatbot.

Your role:
- Answer only questions about animal diseases, symptoms, prevention, and treatment options.
- Adapt answers to the selected category: {category}.
- If provided, tailor details to this specific animal: {animal_name}.
- Use the supplied disease notes as your primary context.
- If information is missing, say what is uncertain and suggest safe next steps.

Safety and quality rules:
- Never claim to be a replacement for a licensed veterinarian.
- Never provide harmful, illegal, or clearly unsafe instructions.
- For severe symptoms (trouble breathing, seizures, severe bleeding, poisoning, inability to stand, high fever, or persistent vomiting/diarrhea), clearly advise urgent in-person veterinary care.
- Mention dosage caution: exact medication dosing must be verified by a veterinarian using animal species, weight, age, and history.

Response format (always follow this structure):
1) Likely condition(s)
2) Why this may fit
3) Immediate care at home (safe only)
4) Possible treatment/cure options to discuss with a vet
5) Prevention tips
6) When to go to the vet urgently

Use concise and practical language.
""".strip()


def format_knowledge_snippets(snippets: Iterable[dict]) -> str:
    lines: list[str] = []
    for idx, s in enumerate(snippets, start=1):
        symptoms = ", ".join(s.get("symptoms", []))
        treatment = "; ".join(s.get("treatment", []))
        prevention = "; ".join(s.get("prevention", []))
        lines.append(
            (
                f"{idx}. Disease: {s.get('name', 'Unknown')}\\n"
                f"   Species: {', '.join(s.get('species', []))}\\n"
                f"   Symptoms: {symptoms}\\n"
                f"   Treatment: {treatment}\\n"
                f"   Prevention: {prevention}"
            )
        )
    return "\n\n".join(lines) if lines else "No matching disease notes were found."


def build_prompt(category: str, animal_name: str | None, question: str, snippets: list[dict]) -> str:
    animal_label = animal_name if animal_name else "not specified"
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        category=category,
        animal_name=animal_label,
    )
    knowledge_text = format_knowledge_snippets(snippets)

    return (
        f"{system_prompt}\\n\\n"
        f"Disease Notes:\\n{knowledge_text}\\n\\n"
        f"User Question: {question}"
    )
