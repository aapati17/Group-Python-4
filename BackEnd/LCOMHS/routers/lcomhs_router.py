from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from typing import Optional

from services.lcomhs_calculator import calculate_lcomhs
from services.project_parser import parse_java_files_in_dir
from services.github_service import fetch_project_from_github, cleanup_dir


router = APIRouter()

@router.post("/calculate")
async def calculate_lcomhs_endpoint(
    gitHubLink: Optional[str] = Form(
        None, description="GitHub URL"
    )
):
    """
    Single endpoint to compute LCOMHS from a GitHub URL.

    Request:
      - multipart/form-data
      - Fields:
        gitHubLink: The GitHub URL

    Response:
      - JSON object with LCOMHS results for each Java class.
    """
    
    temp_dir = None
    
    try:
        if not gitHubLink:
            raise HTTPException(status_code=400, detail="Please provide a GitHub URL in gitHubLink.")

        # Clone the GitHub repo to a temp directory
        temp_dir = fetch_project_from_github(gitHubLink)

        # Parse .java files and compute LCOMHS
        java_classes = parse_java_files_in_dir(temp_dir)
        results = []
        for cls in java_classes:
            lcomhs_value = calculate_lcomhs(cls)
            results.append({"class_name": cls.name, "score": lcomhs_value})

        return {"lcomhs": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_dir:
            cleanup_dir(temp_dir)