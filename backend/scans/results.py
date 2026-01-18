from datetime import datetime, timezone
from scans.repository import get_database
from scans.utils.output import strip_ansi


def build_result(scan_id: str, tool: str, raw_output: str):
    return {
        "scan_id": scan_id,
        "tool": tool,
        "raw_output": raw_output,
        "clean_output": strip_ansi(raw_output),
        "created_at": datetime.now(timezone.utc),
    }


def save_scan_result(result: dict) -> None:
    db = get_database()
    db.results.insert_one(result)
