import docker
from docker.errors import ContainerError
from scans.results import build_result, save_scan_result

client = docker.from_env()


def run_tool(
    scan_id: str,
    tool_name: str,
    command: list[str],
    timeout: int = 300,  # seconds (5 minutes)
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

        result = build_result(
            scan_id=scan_id,
            tool=tool_name,
            raw_output=decoded,
        )
        save_scan_result(result)

    except ContainerError as exc:
        # Tool exited with non-zero code
        decoded = exc.stderr.decode("utf-8", errors="ignore")

        result = build_result(
            scan_id=scan_id,
            tool=tool_name,
            raw_output=decoded,
        )
        save_scan_result(result)
