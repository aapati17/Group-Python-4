import os
import re
import firebase_admin
import time
from firebase_admin import credentials, firestore
from datetime import datetime

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
    repo_url = repo_url.replace(".git", "")
    # remove anything not alphanumeric or underscore
    doc_id = re.sub(r"[^a-zA-Z0-9_]+", "_", repo_url)
    return doc_id.lower()

def store_lcomhs_data_in_firebase(repo_url: str, label_map: dict):
    """
    Stores (or updates) the lcomhs_data for a given repo URL.
    """
    doc_id = to_doc_id(repo_url)
    data = {

        "timestamp": datetime.utcfromtimestamp(time.time()).isoformat() + "Z",
        "data": label_map,
        "gitUniqueId": doc_id,

    }
    db.collection("lcomhs_data").add(data)

def fetch_lcomhs_data_from_firebase(repo_url: str) -> list:
    """
    Gets the lcomhs_data for a given repoUrl.
    Returns a array of data.
    """

    doc_id = to_doc_id(repo_url)

    query = db.collection("lcomhs_data").where("gitUniqueId", "==", doc_id).stream()

    results = []
    for doc in query:
        results.append(doc.to_dict())

    return results