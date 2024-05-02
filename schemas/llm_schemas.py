from pydantic import BaseModel

class PredictionSchema(BaseModel):
    patient_report: dict

class PromptSchema(BaseModel):
    prompt: str


class ContextSchema(BaseModel):
    patient_report: dict
