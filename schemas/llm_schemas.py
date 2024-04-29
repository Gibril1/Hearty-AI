from pydantic import BaseModel

class PredictionSchema(BaseModel):
    confidence: float
    prediction: str

class PromptSchema(BaseModel):
    prompt: str


class ContextSchema(BaseModel):
    context: str
