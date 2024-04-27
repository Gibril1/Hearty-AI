from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.llm_routes import llm_routes

# init app
app = FastAPI()

# register routes
app.include_router(llm_routes)


# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {
        'message': 'Server is working and alive 🥰.',
        'shoutouts': 'Shout outs to Isaac Bcwin 🥰'
    }