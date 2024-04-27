import os
from dotenv import load_dotenv
load_dotenv()
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from schemas.llm_schemas import PredictionSchema

llm = ChatOpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    model='gpt-3.5-turbo',
    temperature=0.2
)
class ModelPredictionService:

    def format_model_response(self, result:PredictionSchema):
        if result.prediction == 1:
            result_output = "You have a heart disease"
        elif result.prediction == 0:
            result_output = "You do not have a heart disease"

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a trained cardiologist. A message would be passed to you to determine the heart status of your patient. Formulate either a congratulatory message or an encouraging message based on your patient: {context}"),
            ("human", "{input}")
        ])


        context = f"{result_output}"

        chain = prompt | llm

        response = chain.invoke({
            'context': context,
            'input': "Can you please tell me the status of my heart"
        })
        return response.content