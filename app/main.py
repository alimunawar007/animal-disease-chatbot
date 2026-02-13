from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .gemini_client import GeminiClient
from .knowledge_base import get_categories, load_knowledge_base, retrieve_diseases
from .models import ChatRequest, ChatResponse
from .prompt_builder import build_prompt

load_dotenv()

app = FastAPI(title="Animal Disease Chatbot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

_knowledge_base = load_knowledge_base()
_gemini: GeminiClient | None = None


def get_gemini_client() -> GeminiClient:
    global _gemini
    if _gemini is None:
        _gemini = GeminiClient(
            api_key=os.getenv("GEMINI_API_KEY"),
            model_name=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        )
    return _gemini


@app.get("/")
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/categories")
def categories() -> dict:
    return {"categories": get_categories(_knowledge_base)}


@app.get("/api/diseases")
def diseases(category: str) -> dict:
    if category not in _knowledge_base:
        raise HTTPException(status_code=400, detail="Invalid category")
    return {
        "category": category,
        "diseases": [item["name"] for item in _knowledge_base[category]],
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    if req.category not in _knowledge_base:
        raise HTTPException(status_code=400, detail="Invalid category selected")

    snippets = retrieve_diseases(
        _knowledge_base,
        category=req.category,
        question=req.question,
        animal_name=req.animal_name,
    )

    prompt = build_prompt(
        category=req.category,
        animal_name=req.animal_name,
        question=req.question,
        snippets=snippets,
    )

    if req.history:
        history_block = "\n\nRecent chat history:\n" + "\n".join(
            f"{m.role}: {m.content}" for m in req.history[-5:]
        )
        prompt = f"{prompt}{history_block}"

    try:
        answer = get_gemini_client().generate(prompt)
    except RuntimeError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err
    except Exception as err:
        # Ensure API errors are always JSON, even when upstream SDK fails.
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response from Gemini: {err}",
        ) from err

    warnings: list[str] = []
    lowered = answer.lower()
    emergency_tokens = ["urgent", "immediately", "emergency", "seizure", "trouble breathing"]
    if any(token in lowered for token in emergency_tokens):
        warnings.append("Possible emergency condition mentioned. Immediate veterinary evaluation is advised.")

    return ChatResponse(
        answer=answer,
        referenced_diseases=[d.get("name", "Unknown") for d in snippets],
        warnings=warnings,
    )
