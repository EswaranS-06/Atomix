import uuid
from datetime import datetime, timezone
from config.db.mongo import get_mongo_client
from scans.apps import ScanState


def get_scans_collection():
    client = get_mongo_client()
    db = client.get_default_database()
    return db.scans


def create_scan(target: str, profile: str) -> dict:
    scan_id = str(uuid.uuid4())

    scan = {
        "scan_id": scan_id,
        "target": target,
        "profile": profile,
        "state": ScanState.CREATED,
        "created_at": datetime.now(timezone.utc),
    }

    collection = get_scans_collection()
    collection.insert_one(scan)

    # IMPORTANT: do not return MongoDB-injected fields
    scan.pop("_id", None)

    return scan

def list_scans() -> list[dict]:
    collection = get_scans_collection()
    scans = []

    for doc in collection.find({}, {"_id": 0}):
        scans.append(doc)

    return scans


def get_scan_by_id(scan_id: str) -> dict | None:
    collection = get_scans_collection()
    doc = collection.find_one({"scan_id": scan_id}, {"_id": 0})
    return doc
