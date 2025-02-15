import json
from fastapi import FastAPI, Form, File
# Adding CORS middleware from FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],  # You can specify specific origins instead of allowing all with "*"
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post("/sample")
async def root(url: str = Form(...), metrics: str = Form(...)):
    return {"url": url, "metrics": metrics}