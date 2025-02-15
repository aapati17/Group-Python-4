from fastapi import FastAPI, Form, File, UploadFile
# Adding CORS middleware from FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

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
async def root(
    sourceType: str = Form(...),
    sourceLink: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    metrics: str = Form(...)
):
    return {
        "sourceType": sourceType,
        "sourceLink": sourceLink,
        "file": file,
        "metrics": metrics
    }