import docker
from docker.errors import ContainerError

from scans.results import build_result, save_scan_result
from scans.generators.whatweb import generate_findings
from scans.generators.nikto import generate_findings as generate_nikto_findings
from scans.findings import save_finding, finding_exists

client = docker.from_env()


def run_tool(
    scan_id: str,
    tool_name: str,
    command: list[str],
    timeout: int = 300,
) -> None:
    """
    Executes a tool inside recon-engine container with timeout.
    """

    try:
        output = client.containers.run(
            image="recon-engine",
            command=command,
            remove=True,
            stdout=True,
            stderr=True,
            detach=False,
            tty=False,
            network_mode="bridge",
        )

        decoded = output.decode("utf-8", errors="ignore")

    except ContainerError as exc:
        # Tool exited with non-zero code
        decoded = exc.stderr.decode("utf-8", errors="ignore")

    # ---- Result persistence (single path, no duplication) ----
    result = build_result(
        scan_id=scan_id,
        tool=tool_name,
        raw_output=decoded,
    )
    save_scan_result(result)

    # ---- Finding generation ----
    if tool_name == "whatweb":
        findings = generate_findings(
            scan_id=scan_id,
            clean_output=result["clean_output"],
        )

    elif tool_name == "nikto":
        findings = generate_nikto_findings(
            scan_id=scan_id,
            clean_output=result["clean_output"],
        )

    else:
        findings = []

    for finding in findings:
        if not finding_exists(
            scan_id=finding["scan_id"],
            tool=finding["tool"],
            evidence=finding["evidence"],
        ):
            save_finding(finding)
