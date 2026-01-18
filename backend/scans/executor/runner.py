import logging

from scans.apps import ScanState
from scans.repository import (
    list_scans,
    update_scan_state,
    mark_scan_completed,
    mark_scan_failed,
)
from scans.executor.docker_runner import run_tool
from scans.profiles import load_profile

logger = logging.getLogger(__name__)


def process_queued_scans():
    """
    Phase 4 executor (profile-driven).
    """

    scans = list_scans()

    for scan in scans:
        if scan.get("state") != ScanState.QUEUED:
            continue

        scan_id = scan["scan_id"]
        target = scan["target"]
        profile_name = scan["profile"]

        logger.info("Executor picked scan %s", scan_id)

        try:
            update_scan_state(scan_id, ScanState.RUNNING)
            logger.info("Scan %s marked as RUNNING", scan_id)

            profile = load_profile(profile_name)

            for tool in profile.get("tools", []):
                tool_name = tool["name"]
                raw_command = tool["command"]

                command = [
                    part.format(target=target)
                    for part in raw_command
                ]

                logger.info(
                    "Running tool %s for scan %s",
                    tool_name,
                    scan_id,
                )

                run_tool(scan_id, tool_name, command)

            mark_scan_completed(scan_id)
            logger.info("Scan %s marked as COMPLETED", scan_id)

        except Exception as exc:
            logger.error("Scan %s failed: %s", scan_id, exc)
            mark_scan_failed(scan_id, str(exc))
