import os
from dotenv import load_dotenv
load_dotenv()
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from fastapi import HTTPException, status
from schemas.llm_schemas import PredictionSchema
from utils.formatting import convert_data

llm = ChatOpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    model='gpt-3.5-turbo',
    temperature=0.2
)
class ModelPredictionService:

    def format_model_response(self, patient_data:PredictionSchema):
        try:
            formatted_data, confidence, prediction = convert_data(patient_data)

            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a trained cardiologist.
                
                Context: {context}
                """),
                ("human", "{input}")
            ])


            context = f"You are trained cardiologist. You are supposed to be more like a virtual assistant to a doctor. In your response, speak as if you are talking to a doctor. Explain what this {formatted_data} means and advice the doctor on what to tell to his patient with these conditions. The data was passed through an AI model and it presented a confidence level of {confidence} and a prediction that {prediction}"

            chain = prompt | llm

            response = chain.invoke({
                'context': context,
                'input': "What practical advise can you give to the doctor?"
            })
            return response.content
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        