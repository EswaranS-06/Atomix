from pydantic import BaseModel
from typing import Dict


class ScanSummarySchema(BaseModel):
    scan_id: str
    total_findings: int
    by_severity: Dict[str, int]
    by_type: Dict[str, int]
    tools: Dict[str, int]
