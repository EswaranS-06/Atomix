from scans.repository import get_database


def build_scan_summary(scan_id: str) -> dict:
    db = get_database()

    findings = list(
        db.findings.find(
            {"scan_id": scan_id},
            {"_id": 0},
        )
    )

    summary = {
        "scan_id": scan_id,
        "total_findings": len(findings),
        "by_severity": {
            "info": 0,
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0,
        },
        "by_type": {},
        "tools": {},
    }

    for finding in findings:
        # ---- Severity aggregation ----
        severity = finding.get("severity", "info")
        if severity in summary["by_severity"]:
            summary["by_severity"][severity] += 1

        # ---- Type aggregation ----
        ftype = finding.get("type", "unknown")
        summary["by_type"][ftype] = summary["by_type"].get(ftype, 0) + 1

        # ---- Tool aggregation ----
        tool = finding.get("tool", "unknown")
        summary["tools"][tool] = summary["tools"].get(tool, 0) + 1

    return summary
