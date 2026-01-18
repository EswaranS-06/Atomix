from scans.findings import build_finding


def generate_findings(scan_id: str, clean_output: str) -> list[dict]:
    """
    Extremely conservative WhatWeb finding generator.
    Only extracts high-confidence observations.
    """
    findings = []

    if "HTTPServer[" in clean_output:
        # Example: HTTPServer[cloudflare]
        for line in clean_output.splitlines():
            if "HTTPServer[" not in line:
                continue

            server = line.split("HTTPServer[", 1)[1].split("]", 1)[0]

            findings.append(
                build_finding(
                    scan_id=scan_id,
                    tool="whatweb",
                    title="Web Server Identified",
                    description=f"Web server technology detected: {server}",
                    evidence=f"HTTPServer[{server}]",
                    severity="info",
                )
            )

    return findings
