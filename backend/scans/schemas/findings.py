from datetime import datetime
from pydantic import BaseModel, Field


class FindingSchema(BaseModel):
    scan_id: str
    tool: str
    type: str
    title: str
    description: str
    severity: str = Field(
        pattern="^(info|low|medium|high|critical)$"
    )
    evidence: str
    created_at: datetime

class FindingsResponseSchema(BaseModel):
    scan_id: str
    count: int
    findings: list[FindingSchema]
