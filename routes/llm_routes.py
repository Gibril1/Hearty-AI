from fastapi import APIRouter, status
from pydantic import BaseModel
from services.prediction_service import ModelPredictionService

class PredictionData(BaseModel):
    prediction: int

prediction_model = ModelPredictionService()

llm_routes = APIRouter(
    prefix='/api/v1/llm',
    tags=['LLM Chat Bot']
)

@llm_routes.post('/predict', status_code=status.HTTP_200_OK)
def make_model_prediction(prediction_data:PredictionData):
    return prediction_model.format_model_response(prediction_data)
