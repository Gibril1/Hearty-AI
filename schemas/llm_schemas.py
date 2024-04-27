from pydantic import BaseModel

class PredictionSchema(BaseModel):
    prediction: int

class PromptSchema(BaseModel):
    prompt: str
