import os
from fastapi import APIRouter, HTTPException, Form, Body, Query
from typing import Optional, Dict
from services.defect_score_calculator import compute_defect_score_from_github
from services.firebase_service import store_label_mapping_in_firebase, fetch_label_mapping_from_firebase

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
        return result

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
def store_labels_for_project(
    sourceValue: str = Query(..., example="https://github.com/owner/repo")
):
    """
    Get custom label -> severity mapping from Firebase for a given repo URL.
    """
    try:
        label_mapping = fetch_label_mapping_from_firebase(sourceValue)
        return label_mapping
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))