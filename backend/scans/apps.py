from django.apps import AppConfig


class ScansConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "scans"


class ScanState:
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    ALL = {
        CREATED,
        QUEUED,
        RUNNING,
        COMPLETED,
        FAILED,
    }

