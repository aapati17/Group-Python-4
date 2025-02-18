from fastapi import FastAPI, HTTPException, Body
import httpx  # We'll use httpx or requests to call the LCOM4 service
import os
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI(title="API Gateway (Middleware)")

# We'll read LCOM4 service URL from an ENV variable or default
LCOM4_URL = os.environ.get("LCOM4_SERVICE_URL", "http://lcom4:8000")  

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],  # You can specify specific origins instead of allowing all with "*"
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Mock Endpoint
@app.get("/")
def read_root():
    return {"message": "API Gateway up and running"}


@app.post("/gateway/calculate")
async def gateway_lcom4(
    gitHubLink: str, 
    metrics: str
    ):
    """
    Proxies the file to the LCOM4 microservice's /api/lcom4/calculate endpoint.
    """

    selectedMetrics = metrics.split(",")
    results = {}

    if "LCOM4" in selectedMetrics:
        async with httpx.AsyncClient() as client:
            formdata = {
                "sourceType": "git",
                "gitHubLink": gitHubLink
            }
            lcom4_response = await client.post(f"{LCOM4_URL}/api/lcom4/calculate", data=formdata, timeout=None)
        
        if lcom4_response.status_code != 200:
            raise HTTPException(
                status_code=500, 
                detail=f"LCOM4 call failed: {lcom4_response.status_code}, {lcom4_response.text}"
            )
        
        results["LCOM4"] = lcom4_response.json()

    else:
        results["LCOM4"] = None
    
    return results
    # Make a request to LCOM4 container
    # We'll do a multipart/form-data request with httpx
    # async with httpx.AsyncClient() as client:
    #     formdata = {
    #         "sourceType": "git",
    #         "gitHubLink": gitHubLink
    #     }
    #     lcom4_response = await client.post(f"{LCOM4_URL}/api/lcom4/calculate", data=formdata, timeout=None)
    
    # if lcom4_response.status_code != 200:
    #     raise HTTPException(
    #         status_code=500, 
    #         detail=f"LCOM4 call failed: {lcom4_response.status_code}, {lcom4_response.text}"
    #     )
    
    # return lcom4_response.json()