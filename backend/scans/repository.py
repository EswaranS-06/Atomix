import uuid
from datetime import datetime, timezone
from scans.apps import ScanState

from pymongo import MongoClient
from django.conf import settings

_client = None


def get_database():
    global _client

    if _client is None:
        _client = MongoClient(settings.MONGO_URI)

    return _client[settings.MONGO_DB_NAME]

def get_scans_collection():
    db = get_database()
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

from scans.apps import ScanTransitions
from datetime import datetime, timezone


def update_scan_state(scan_id: str, new_state: str) -> dict | None:
    collection = get_scans_collection()

    scan = collection.find_one({"scan_id": scan_id})
    if not scan:
        return None

    current_state = scan.get("state")
    allowed = ScanTransitions.ALLOWED.get(current_state, set())

    if new_state not in allowed:
        raise ValueError(
            f"Invalid state transition: {current_state} → {new_state}"
        )

    update = {
        "$set": {
            "state": new_state,
            "updated_at": datetime.now(timezone.utc),
        }
    }

    collection.update_one({"scan_id": scan_id}, update)

    # Return updated scan (API-safe)
    updated = collection.find_one(
        {"scan_id": scan_id},
        {"_id": 0},
    )

    return updated

def mark_scan_completed(scan_id: str) -> dict | None:
    return update_scan_state(scan_id, ScanState.COMPLETED)


def mark_scan_failed(scan_id: str, reason: str) -> dict | None:
    collection = get_scans_collection()

    scan = collection.find_one({"scan_id": scan_id})
    if not scan:
        return None

    current_state = scan.get("state")
    allowed = ScanTransitions.ALLOWED.get(current_state, set())

    if ScanState.FAILED not in allowed:
        raise ValueError(
            f"Invalid state transition: {current_state} → FAILED"
        )

    update = {
        "$set": {
            "state": ScanState.FAILED,
            "error": reason,
            "updated_at": datetime.now(timezone.utc),
        }
    }

    collection.update_one({"scan_id": scan_id}, update)

    return collection.find_one(
        {"scan_id": scan_id},
        {"_id": 0},
    )

