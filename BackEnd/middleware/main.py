import sys
sys.path.append('..')
from fastapi import FastAPI, Form, File, UploadFile
from LCOM4.routers.lcom4_router import router as lcom4_router
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi.testclient import TestClient

app = FastAPI()

# Include the LCOM4 router
app.include_router(lcom4_router, prefix="/api/lcom4", tags=["LCOM4"])

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],  # You can specify specific origins instead of allowing all with "*"
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

client = TestClient(app)

@app.post("/")
async def root(
    sourceType: str = Form(...),
    githubLink: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    metrics: str = Form(...)
):
    selectedMetrics = metrics.split(',')
    if 'LCOM4' in selectedMetrics:
        formData = {
            "sourceType": sourceType,
            "gitHubLink": githubLink,
        }
        response = client.post("/api/lcom4/calculate", data=formData)
        return response.json()
    else:
        return {
            "message": "No metrics selected."
        }