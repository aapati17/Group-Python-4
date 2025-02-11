from fastapi import FastAPI
# Adding CORS middleware from FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Initial Setup"}

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # You can specify specific origins instead of allowing all with "*"
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)