from fastapi import FastAPI, HTTPException, Body, Query
import httpx
import os
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import asyncio

app = FastAPI(title="API Gateway (Middleware)")

# We'll read service URLs from ENV or default
LCOM4_URL = os.environ.get("LCOM4_SERVICE_URL", "http://lcom4:8000")
LCOMHS_URL = os.environ.get("LCOMHS_URL", "http://lcomhs:8000")
DEFECT_SCORE_URL = os.environ.get("DEFECT_SCORE_URL", "http://defectscore:8000")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # You can specify specific origins instead of allowing all with "*"
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Mock Endpoint
@app.get("/")
def read_root():
    return {"message": "API Gateway up and running"}


@app.post("/gateway/calculate")
async def gateway_calculate(
    gitHubLink: str = Body(..., example="https://github.com/owner/repo"),
    metrics: str = Body(..., example="LCOM4,DefectScore,LCOMHS")
):
    """
    Receives a GitHub repository link and a comma-separated list of metrics to be calculated.
    It then calls the corresponding microservices concurrently and returns a combined result.
    """
    selected_metrics = [m.strip() for m in metrics.lower().split(",")]
    results = {}

    # Create a single AsyncClient to use for all service calls.
    async with httpx.AsyncClient() as client:
        tasks = []

        if "lcom4" in selected_metrics:
            tasks.append(call_lcom4(client, gitHubLink))
        else:
            results["LCOM4"] = None

        if "defectscore" in selected_metrics:
            tasks.append(call_defect_score(client, gitHubLink))
        else:
            results["DefectScore"] = None

        if "lcomhs" in selected_metrics:
            tasks.append(call_lcomhs(client, gitHubLink))
        else:
            results["LCOMHS"] = None

        # Run all tasks concurrently.
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    # Process each response from the tasks.
    for resp in responses:
        if isinstance(resp, Exception):
            # If any call fails, raise an exception.
            raise HTTPException(status_code=500, detail=str(resp))
        else:
            results.update(resp)

    return results

# Helper functions to call each microservice

async def call_lcom4(client: httpx.AsyncClient, gitHubLink: str) -> dict:
    formdata = {
        "gitHubLink": gitHubLink
    }
    response = await client.post(f"{LCOM4_URL}/api/lcom4/calculate", data=formdata, timeout=None)
    if response.status_code != 200:
        raise Exception(f"LCOM4 call failed: {response.status_code}, {response.text}")
    return {"LCOM4": response.json()}

async def call_defect_score(client: httpx.AsyncClient, gitHubLink: str) -> dict:
    formdata = {
        "sourceValue": gitHubLink
    }
    response = await client.post(f"{DEFECT_SCORE_URL}/api/defect_score/calculate", data=formdata, timeout=None)
    if response.status_code != 200:
        raise Exception(f"DefectScore call failed: {response.status_code}, {response.text}")
    return {"DefectScore": response.json()}

async def call_lcomhs(client: httpx.AsyncClient, gitHubLink: str) -> dict:
    formdata = {
        "gitHubLink": gitHubLink
    }
    response = await client.post(f"{LCOMHS_URL}/api/lcomhs/calculate", data=formdata, timeout=None)
    if response.status_code != 200:
        raise Exception(f"LCOMHS call failed: {response.status_code}, {response.text}")
    return {"LCOMHS": response.json()}


@app.post("/gateway/defectscore/labelmapping")
async def gateway_get_defectscore_labelmapping(
    gitHubLink: str = Body(..., example="https://github.com/owner/repo"),
    labelSeverityMap: Dict[str, int] = Body(..., example={"bug": 2, "critical": 5})
    ):
    """
    Post the label mapping data to database using Defect Score service
    """

    results = {}

    async with httpx.AsyncClient() as client:
        label_data = {
            "sourceValue": gitHubLink,
            "labelSeverityMap": labelSeverityMap

        }
        labelmapping_response = await client.post(f"{DEFECT_SCORE_URL}/api/defect_score/labelsMapping", json=label_data, timeout=None)

    if labelmapping_response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"defectscore post label mapping call failed: {labelmapping_response.status_code}, {labelmapping_response.text}"
        )
    
    results = labelmapping_response.json()
    return results

@app.get("/gateway/defectscore/labelmapping")
async def gateway_get_defectscore_labelmapping(
    gitHubLink: str = Query(..., example="URL For the GitHub Repository")
    ):
    """
    Get the label mapping data from database from Defect Score service
    """

    results = {}

    async with httpx.AsyncClient() as client:
        param_data = {
            "sourceValue": gitHubLink
        }
        labelmapping_response = await client.get(f"{DEFECT_SCORE_URL}/api/defect_score/labelsMapping", params=param_data, timeout=None)

    if labelmapping_response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"defectscore get label mapping call failed: {labelmapping_response.status_code}, {labelmapping_response.text}"
        )
    
    results = labelmapping_response.json()
    return results