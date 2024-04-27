from fastapi import FastAPI
from routes.llm_routes import llm_routes

# init app
app = FastAPI()

# register routes
app.include_router(llm_routes)