from datetime import datetime, timezone
from scans.repository import get_database


def build_finding(
    scan_id: str,
    tool: str,
    title: str,
    description: str,
    evidence: str,
    severity: str = "info",
    finding_type: str = "observation",
) -> dict:
    """
    Build a generic finding object.

    This function does NOT parse tool output.
    It only structures already-known information.
    """
    return {
        "scan_id": scan_id,
        "tool": tool,
        "type": finding_type,
        "title": title,
        "description": description,
        "severity": severity,
        "evidence": evidence,
        "created_at": datetime.now(timezone.utc),
    }


def save_finding(finding: dict) -> None:
    db = get_database()
    db.findings.insert_one(finding)

def finding_exists(scan_id: str, tool: str, evidence: str) -> bool:
    db = get_database()
    return (
        db.findings.count_documents(
            {
                "scan_id": scan_id,
                "tool": tool,
                "evidence": evidence,
            },
            limit=1,
        )
        > 0
    )
