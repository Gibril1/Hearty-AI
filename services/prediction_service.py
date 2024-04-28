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
        

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a trained cardiologist. A message would be passed to you to determine the heart status of your patient. Formulate either a congratulatory message or an encouraging message based on your patient: {context}"),
            ("human", "{input}")
        ])


        context = f"You are trained cardiologist who gives results on whether a user has a heart disease or not. An AI model predicts this. This is the result. A confidence level of {result.confidence} and a verdict of {result.prediction}"

        chain = prompt | llm

        response = chain.invoke({
            'context': context,
            'input': "Can you please tell me the status of my heart"
        })
        return response.content