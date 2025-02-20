import os
from fastapi import APIRouter, HTTPException, Form, Body, Query
from typing import Optional, Dict
from services.defect_score_calculator import compute_defect_score_from_github
from services.firebase_service import to_doc_id,store_label_mapping_in_firebase,\
    fetch_label_mapping_from_firebase, \
    store_def_score_data_in_firebase, \
    fetch_def_score_data_from_firebase, \
    store_benchmark_in_firebase, \
    get_benchmark_from_firebase
from datetime import datetime
import time

router = APIRouter()

@router.post("/calculate")
async def calculate_defect_score(
    sourceValue: Optional[str] = Form(None, description="GitHub repo URL"),
    token: Optional[str] = Form(None, description="GitHub token if needed for private repos")
):
    """
    Endpoint to compute a 'defect score' by retrieving issues from a GitHub repo
    """

    try:
        if not sourceValue:
            raise HTTPException(
                status_code=400, 
                detail="Please provide a GitHub repo URL in sourceValue"
            )

        # If no token provided in the request, try environment variable
        if not token:
            token = os.getenv("GITHUB_TOKEN", None)

        # Compute the defect score from the GH Issues
        result = compute_defect_score_from_github(sourceValue, token)

        history_data = fetch_def_score_data_from_firebase(sourceValue)
        current_timestamp = datetime.utcfromtimestamp(time.time()).isoformat() + "Z"

        current_data = {
            "timestamp": current_timestamp,
            "data": result,
            "gitUniqueId": to_doc_id(sourceValue)   
        }

        store_def_score_data_in_firebase(sourceValue, result)

        return { "defect_score_history": history_data if history_data else [],
                 "current_defect_score": current_data }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/labelsMapping")
def store_labels_for_project(
    sourceValue: str = Body(..., example="https://github.com/owner/repo"),
    labelSeverityMap: Dict[str, int] = Body(..., example={"bug": 2, "critical": 5})
):
    """
    Stores custom label -> severity mapping in Firebase for a given repo URL.
    """
    try:
        store_label_mapping_in_firebase(sourceValue, labelSeverityMap)
        return {"message": "Label severity map stored successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/labelsMapping")
def fetch_labels_for_project(
    sourceValue: str = Query(..., example="https://github.com/owner/repo")
):
    """
    Get custom label -> severity mapping from Firebase for a given repo URL.
    """
    try:
        label_mapping = fetch_label_mapping_from_firebase(sourceValue)
        if not label_mapping:
            return {
            "bug": 2,
            "minor": 2,
            "major": 4,
            "critical": 5,
            "high": 5,
            "low": 1
        }
        return label_mapping
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/benchmark")
def store_labels_for_project(
    sourceValue: str = Body(..., example="https://github.com/owner/repo"),
    benchmark: int = Body(..., example=1)
):
    """
    Stores custom benchmark -> user entered bench mark in Firebase for a given repo URL.
    """
    try:
        store_benchmark_in_firebase(sourceValue, benchmark)
        return {"message": "benchmark stored successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/benchmark")
def store_labels_for_project(
    sourceValue: str = Query(..., example="https://github.com/owner/repo")
):
    """
    get benchmark -> benchmark from Firebase for a given repo URL.
    """
    try:
        benchmark = get_benchmark_from_firebase(sourceValue)
        return {"defect_score_benchmark": benchmark}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))