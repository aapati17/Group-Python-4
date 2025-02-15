import tempfile
import shutil
import zipfile
import subprocess

def fetch_project_from_github(github_url: str) -> str:
    """
    Clones a GitHub repository into a temporary directory and returns the local path.
    """
    temp_dir = tempfile.mkdtemp(prefix="repo_")

    try:
        subprocess.run(["git", "clone", github_url, temp_dir], check=True)
    except subprocess.CalledProcessError as e:
        #  if clone fails
        cleanup_dir(temp_dir)
        raise RuntimeError(f"Failed to clone {github_url}: {e}")

    return temp_dir

def unzip_project(zip_file_path: str) -> str:
    """
    Extracts the given zip file into a temporary directory, 
    and returns the path to the extracted folder.
    """
    temp_dir = tempfile.mkdtemp(prefix="unzip_")
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
    except Exception as e:
        #  if unzip fails
        cleanup_dir(temp_dir)
        raise RuntimeError(f"Error extracting zip file {zip_file_path}: {e}")
    
    return temp_dir

def cleanup_dir(path: str):
    """
    Removes the temporary project directory to free up space.
    """
    shutil.rmtree(path, ignore_errors=True)
