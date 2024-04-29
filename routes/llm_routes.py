from fastapi import APIRouter, status
from services.prediction_service import ModelPredictionService
from services.chat_bot_service import ChatBotService
from schemas.llm_schemas import PredictionSchema, PromptSchema, ContextSchema

prediction_model = ModelPredictionService()
chat = ChatBotService()


llm_routes = APIRouter(
    prefix='/api/v1/llm',
    tags=['LLM Chat Bot']
)

@llm_routes.post('/predict', status_code=status.HTTP_200_OK)
def make_model_prediction(prediction_data:PredictionSchema):
    return prediction_model.format_model_response(prediction_data)

@llm_routes.post('/chat', status_code=status.HTTP_200_OK)
def chat_bot(user_prompt:PromptSchema, prediction_data:PredictionSchema):
    return chat.chat_with_bot(user_prompt, prediction_data)

@llm_routes.post('/history', status_code=status.HTTP_200_OK)
def chat_bot_plus_history(user_prompt:PromptSchema, context_schema:ContextSchema, chat_id:str):
    return chat.chat_with_bot_plus_history(user_prompt, context_schema, chat_id)
