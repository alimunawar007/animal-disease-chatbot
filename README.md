# Animal Disease Chatbot (Gemini + FastAPI)

A complete chatbot project for animal diseases and cure/treatment guidance.

## Features
- Gemini API powered responses
- Category-aware behavior:
  - `mammals`
  - `herbivorous`
  - `carnivorous`
  - `reptiles`
- Built-in disease knowledge base with symptom/treatment/prevention notes
- Safe-answer prompt with emergency and dosage guardrails
- Web UI + REST API

## Project Structure
- `app/main.py`: FastAPI app and API routes
- `app/gemini_client.py`: Gemini integration
- `app/prompt_builder.py`: Core prompt template and runtime prompt builder
- `app/knowledge_base.py`: Disease retrieval logic
- `app/data/diseases.json`: Animal disease data
- `app/static/index.html`: Web chat UI
- `PROMPT.md`: Reusable master prompt

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add env variables:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` and set your Gemini key:
   ```env
   GEMINI_API_KEY=your_real_key
   GEMINI_MODEL=gemini-1.5-flash
   APP_HOST=127.0.0.1
   APP_PORT=8000
   ```

## Run
```bash
uvicorn app.main:app --reload --host ${APP_HOST:-127.0.0.1} --port ${APP_PORT:-8000}
```

Open:
- `http://127.0.0.1:8000`

## API Endpoints
- `GET /api/categories`
- `GET /api/diseases?category=mammals`
- `POST /api/chat`

Sample request:
```json
{
  "category": "mammals",
  "animal_name": "dog",
  "question": "My dog has vomiting and bloody diarrhea. What could it be and what should I do?",
  "history": []
}
```

## Notes
- This app provides educational support, not a medical diagnosis.
- In emergencies, seek immediate veterinary care.
