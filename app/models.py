from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str


class ChatRequest(BaseModel):
    category: str = Field(description="One of mammals, herbivorous, carnivorous, reptiles")
    animal_name: str | None = Field(default=None, description="Specific animal, e.g., dog, cow, snake")
    question: str
    history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    referenced_diseases: list[str]
    warnings: list[str]
