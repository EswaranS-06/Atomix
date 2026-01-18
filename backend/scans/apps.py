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

class ScanTransitions:
    ALLOWED = {
        ScanState.CREATED: {ScanState.QUEUED},
        ScanState.QUEUED: {ScanState.RUNNING},
        ScanState.RUNNING: {ScanState.COMPLETED, ScanState.FAILED},
        ScanState.COMPLETED: set(),
        ScanState.FAILED: set(),
    }
