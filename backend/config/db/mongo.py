import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def get_mongo_client():
    host = os.getenv("MONGO_HOST")
    port = os.getenv("MONGO_PORT")
    db = os.getenv("MONGO_DB")
    user = os.getenv("MONGO_USER")
    password = os.getenv("MONGO_PASSWORD")

    missing = [k for k in [
        "MONGO_HOST", "MONGO_PORT", "MONGO_DB", "MONGO_USER", "MONGO_PASSWORD"
    ] if not os.getenv(k)]

    if missing:
        raise RuntimeError(f"Missing MongoDB environment variables: {missing}")

    uri = (
        f"mongodb://{user}:{password}@"
        f"{host}:{port}/{db}?authSource=admin"
    )

    return MongoClient(uri, serverSelectionTimeoutMS=5000)


def verify_mongo_connection():
    client = get_mongo_client()
    try:
        client.admin.command("ping")
    except ConnectionFailure as exc:
        raise RuntimeError("MongoDB connection failed") from exc
