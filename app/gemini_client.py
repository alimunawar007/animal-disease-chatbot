from __future__ import annotations

import os

import google.generativeai as genai


class GeminiClient:
    def __init__(self, api_key: str | None = None, model_name: str | None = None):
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY is not set. Add it to .env.")

        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 8000,
            },
        )
        text = getattr(response, "text", None)
        if not text:
            return "I could not generate a response right now. Please try again."
        return text.strip()
