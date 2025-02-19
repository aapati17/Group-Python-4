import os
import re
import firebase_admin
import time
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

def store_lcom4_data_in_firebase(repo_url: str, label_map: dict):
    """
    Stores (or updates) the lcom4_data for a given repo URL.
    """
    doc_id = to_doc_id(repo_url)
    data = {

        "timestamp": time.time() ,
        "data": label_map
        "gitUniqueId": doc_id

    }
    db.collection("lcom4_data").document(doc_id).set(data)

def fetch_lcom4_Data_from_firebase(repo_url: str) -> dict:
    """
    Gets the lcom4_data for a given repoUrl.
    Returns a dict of data.
    """
    doc_id = to_doc_id(repo_url)
    doc_ref = db.collection("lcom4_data").document(doc_id)
    doc = doc_ref.get()

    data = doc.to_dict()
    return data.get("lcom4_data", {})