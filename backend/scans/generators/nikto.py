from scans.findings import build_finding


SECURITY_HEADERS = {
    "content-security-policy",
    "strict-transport-security",
    "x-content-type-options",
    "referrer-policy",
    "permissions-policy",
}


def generate_findings(scan_id: str, clean_output: str) -> list[dict]:
    findings = []

    for line in clean_output.splitlines():

        # ---- Missing security headers ----
        if "Suggested security header missing:" in line:
            header = line.split("missing:", 1)[1].split(".", 1)[0].strip()

            if header.lower() in SECURITY_HEADERS:
                findings.append(
                    build_finding(
                        scan_id=scan_id,
                        tool="nikto",
                        finding_type="misconfiguration",
                        title="Missing Security Header",
                        description=f"Security header '{header}' is not set",
                        evidence=line.strip(),
                        severity="low",
                    )
                )

        # ---- Server banner observation ----
        if line.startswith("+ Server:"):
            server = line.split(":", 1)[1].strip()

            findings.append(
                build_finding(
                    scan_id=scan_id,
                    tool="nikto",
                    finding_type="observation",
                    title="Web Server Banner",
                    description=f"Web server banner identified: {server}",
                    evidence=line.strip(),
                    severity="info",
                )
            )

        # ---- Execution limits / errors ----
        if "ERROR: Host maximum execution time" in line:
            findings.append(
                build_finding(
                    scan_id=scan_id,
                    tool="nikto",
                    finding_type="execution",
                    title="Nikto Scan Timed Out",
                    description="Nikto scan reached its maximum execution time",
                    evidence=line.strip(),
                    severity="info",
                )
            )

    return findings
