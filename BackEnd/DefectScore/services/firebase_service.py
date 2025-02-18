import os
import re
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDS", "serviceAccountKey.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def to_doc_id(repo_url: str) -> str:
    """
    Convert 'https://github.com/owner/repo' -> 'owner_repo'
    or some sanitized doc ID for Firestore.
    """
    repo_url = repo_url.replace("https://github.com/", "")
    # remove anything not alphanumeric or underscore
    doc_id = re.sub(r"[^a-zA-Z0-9_]+", "_", repo_url)
    return doc_id.lower()

def store_label_mapping_in_firebase(repo_url: str, label_map: dict):
    """
    Stores (or updates) the labelSeverityMap for a given repo URL.
    """
    doc_id = to_doc_id(repo_url)
    data = {
        "repoUrl": repo_url,
        "labelSeverityMap": label_map
    }
    db.collection("project_severity_maps").document(doc_id).set(data)

def fetch_label_mapping_from_firebase(repo_url: str) -> dict:
    """
    Gets the labelSeverityMap for a given repoUrl.
    Returns a dict of label->severity, or raises an error if not found.
    """
    doc_id = to_doc_id(repo_url)
    doc_ref = db.collection("project_severity_maps").document(doc_id)
    doc = doc_ref.get()
    if not doc.exists:
        label_severity_map = {
            "bug": 2,
            "minor": 2,
            "major": 4,
            "critical": 5,
            "high": 5,
            "low": 1
        }
        return label_severity_map
    data = doc.to_dict()
    return data.get("labelSeverityMap", {})