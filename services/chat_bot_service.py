import os
import logging
from dotenv import load_dotenv
load_dotenv()
import redis
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from schemas.llm_schemas import PredictionSchema, PromptSchema, ContextSchema
from utils.formatting import convert_data
from fastapi import HTTPException, status
from langchain_community.chat_message_histories.upstash_redis import (
    UpstashRedisChatMessageHistory
)

# init logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Init redis: Redis would be used for our persistent data storage for our chat history and memory purposes
redis_cache = redis.Redis(
  host=os.getenv('REDIS_HOST'),
  port=42786,
  password=os.getenv('REDIS_PASSWORD'),
  ssl=True
)

# Upstash redis: It was supposed to be used to handle our history messages but it did not work for our usecases. I left it here for presentation purposes
history = UpstashRedisChatMessageHistory(
    url=os.getenv('REDIS_HOST'),
    token=os.getenv('REDIS_TOKEN'),
    session_id='2626262655454535366363',
    ttl=0
)

# Init GPT Model: This is our chat completion model
llm = ChatOpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    model='gpt-3.5-turbo',
    temperature=0.4
)

class ChatBotService:
    def chat_with_bot(self, user_prompt:PromptSchema, context:PredictionSchema):
        try:
            if context.prediction == 1:
                context_result = "I have a heart disease"
            elif context.prediction == 0:
                context_result = "I do not have a heart disease"
            
            
            prompt = ChatPromptTemplate.from_messages([
                ('system', 'You are a trained cardiologist, who has the ability to give practical advice on heart related device. You can tell whether a user has a heart disease or not.A user had provided you with {context}. You are able to advice the user on what to do next. Be as kind as possible. Be as concise as possible with your response'),
                MessagesPlaceholder(variable_name='chat_history'),
                ('human', '{input}')
            ])

            # chain the prompt to the llm
            chain = prompt | llm
            
            
            chat_history = history.messages


            ai_response = chain.invoke({
                'input': user_prompt.prompt,
                'context': context_result,
                'chat_history': chat_history
            })
            history.add_user_message(user_prompt.prompt)
            history.add_ai_message(ai_response.content)

            return ai_response.content
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    


    def chat_with_bot_plus_history(self, user_prompt:PromptSchema, context:ContextSchema, user_id:str):
        try:
            formatted_data, confidence, prediction = convert_data(context)


            prompt = ChatPromptTemplate.from_messages([
                ('system', '{context}'),
                MessagesPlaceholder(variable_name='chat_history'),
                ('human', '{input}')
            ])


            # # chain the prompt to the llm
            chain = prompt | llm
            logging.info('Prompt has been passed on to the LLM')
            
            # # let us work on getting chat history
            chat_history = redis_cache.lrange(user_id, 0, -1)
            if not chat_history:
                chat_history_array = []
            

            chat_history_array = [message.decode('utf-8') for message in chat_history]
            
            
            context = f"You are trained cardiologist. You are supposed to be more like a virtual assistant to a doctor. In your response, speak as if you are talking to a patient. Explain what this {formatted_data} means and advice the patient on what to do. You are supposed to help the patient navigate through anything related to the heart and the diseases. The data was passed through an AI model and it presented a confidence level of {confidence} and a prediction that {prediction}"

            response = chain.invoke(
            {"context": context, "input": user_prompt.prompt, "chat_history": chat_history_array},
            )

            redis_cache.rpush(user_id, user_prompt.prompt)
            redis_cache.rpush(user_id, response.content)

            chat_history = redis_cache.lrange(user_id, 0, -1)
            logging.info(f'The user prompt is {user_prompt.prompt}')
            logging.info(f'The LLM response is {response.content}')



            return response.content
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
            # return formatted_data, confidence, prediction
