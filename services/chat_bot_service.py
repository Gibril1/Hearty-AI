import os
from dotenv import load_dotenv
load_dotenv()
import redis
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from schemas.llm_schemas import PredictionSchema, PromptSchema
from langchain_community.chat_message_histories.upstash_redis import (
    UpstashRedisChatMessageHistory
)


# Init redis: Redis would be used for our persistent data storage for our chat history and memory purposes
redis_cache = redis.Redis(
  host=os.getenv('REDIS_HOST'),
  port=42786,
  password=os.getenv('REDIS_PASSWORD'),
  ssl=True
)

# Upstash redis: It was supposed to be used to handle our history messages but it did not work for our usecases. I left it there for presentation purposes
history = UpstashRedisChatMessageHistory(
    url=os.getenv('REDIS_HOST'),
    token=os.getenv('REDIS_TOKEN'),
    session_id='2626262655454535366363',
    ttl=0
)

# Init GPT Model: This is our chat completion model
llm = ChatOpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    temperature=0.4
)

class ChatBotService:
    def chat_with_bot(self, user_prompt:PromptSchema, context:PredictionSchema):
        if context.prediction == 1:
            context_result = "You have a heart disease"
        elif context.prediction == 0:
            context_result = "You do not have a heart disease"
        
        
        prompt = ChatPromptTemplate.from_messages([
            ('system', 'You are a trained cardiologist, who has the ability to give practical advice on heart related device. Based on {context}. You are able to advice users on what to do next. Be as kind as possible. And for users who do not have a heart disease, you can be jovial.Be as concise as possible with your response'),
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
    


    def chat_with_bot_plus_history(self, user_prompt:PromptSchema,context:PredictionSchema, user_id:str):
        if context.prediction == 1:
            context_result = "I have a heart disease"
        elif context.prediction == 0:
            context_result = "I do not have a heart disease"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system","""You are a trained cardiologist. A message would be passed to you to determine the heart status of your patient.  {context}
             
            With the information provided to you, respond to the user's heart related problems
             
             """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])


        # chain the prompt to the llm
        chain = prompt | llm

        
        # let us work on getting chat history
        chat_history = redis_cache.get(user_id)
        if not chat_history:
            chat_history = redis_cache.set(user_id, '')
        

        bytes_to_string = redis_cache.get(user_id).decode('utf8')
        chat_history_array = bytes_to_string.split(',')
        
        response = chain.invoke(
        {"context": context_result, "input": user_prompt.prompt, "chat_history": chat_history_array},
        )

        redis_cache.append(user_id, ', ' + user_prompt.prompt)
        redis_cache.append(user_id, ', ' + response.content)

        return response.content
    

