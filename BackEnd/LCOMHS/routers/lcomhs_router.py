from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from typing import Optional
import os
import tempfile

from LCOMHS.services.lcomhs_calculator import calculate_lcomhs
from LCOMHS.services.project_parser import parse_java_files_in_dir

from common_utils.project_fetcher import fetch_project_from_github, unzip_project, cleanup_dir

router = APIRouter()

@router.post("/calculate")
async def calculate_lcomhs_endpoint(
    sourceType: str = Form(..., description="Either 'git' or 'zip'"),
    gitHubLink: Optional[str] = Form(
        None, description="GitHub URL if sourceType='git'. Ignored otherwise."
    ),
    file: Optional[UploadFile] = File(
        None, description="ZIP file if sourceType='zip'. Ignored otherwise."
    )
):
    """
    Single endpoint to compute LCOMHS from either a GitHub URL or a ZIP file.

    Request:
      - multipart/form-data
      - Fields:
         1) sourceType: "git" or "zip"
         2) gitHubLink: The GitHub URL if sourceType="git"
         3) file: The uploaded .zip file if sourceType="zip"

    Response:
      - JSON object with LCOMHS results for each Java class.
    """
    temp_dir = None
    temp_zip_path = None

    # Validate input
    if sourceType not in ["git", "zip"]:
        raise HTTPException(status_code=400, detail="Invalid sourceType. Must be 'git' or 'zip'.")

    # Fetch or Unzip the project
    try:
        if sourceType == "git":
            if not gitHubLink:
                raise HTTPException(status_code=400, detail="Please provide a GitHub URL in gitHubLink.")

            # Clone the GitHub repo to a temp directory
            temp_dir = fetch_project_from_github(gitHubLink)

        elif sourceType == "zip":
            if file is None:
                raise HTTPException(status_code=400, detail="Please upload a .zip file.")
            if not file.filename.endswith(".zip"):
                raise HTTPException(status_code=400, detail="File must be .zip")

            # Save uploaded file to a temp path
            temp_zip_path = os.path.join(tempfile.gettempdir(), file.filename)
            with open(temp_zip_path, "wb") as f:
                f.write(await file.read())

            # Unzip the project
            temp_dir = unzip_project(temp_zip_path)

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
        if temp_zip_path and os.path.exists(temp_zip_path):
            os.remove(temp_zip_path)
        if temp_dir:
            cleanup_dir(temp_dir)