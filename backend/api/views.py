import os
from django.http import JsonResponse, Http404
from config.profiles.loader import load_profile, ProfileError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from scans.repository import create_scan
from config.profiles.loader import load_profile, ProfileError

from scans.schemas.findings import FindingsResponseSchema
from scans.schemas.summary import ScanSummarySchema

def list_profiles(request):
    profiles_dir = os.getenv("PROFILES_DIR", "profiles")

    if not os.path.isdir(profiles_dir):
        return JsonResponse(
            {"error": "Profiles directory not found"},
            status=500,
        )

    profiles = []
    for fname in os.listdir(profiles_dir):
        if fname.endswith(".yaml"):
            profiles.append(fname.replace(".yaml", ""))

    return JsonResponse(
        {
            "profiles": sorted(profiles)
        }
    )


def get_profile(request, name: str):
    try:
        profile = load_profile(name)
    except ProfileError as exc:
        raise Http404(str(exc))

    return JsonResponse(profile)

@csrf_exempt
def create_scan_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    target = payload.get("target")
    profile_name = payload.get("profile", "default")

    if not target:
        return JsonResponse({"error": "target is required"}, status=400)

    try:
        load_profile(profile_name)
    except ProfileError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    scan = create_scan(target=target, profile=profile_name)
    return JsonResponse(scan, status=201)

from scans.repository import list_scans, get_scan_by_id


def list_scans_view(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    scans = list_scans()
    return JsonResponse({"scans": scans})


def get_scan_view(request, scan_id: str):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    scan = get_scan_by_id(scan_id)
    if not scan:
        return JsonResponse({"error": "Scan not found"}, status=404)

    return JsonResponse(scan)

from scans.apps import ScanState
from scans.repository import update_scan_state
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def queue_scan_view(request, scan_id: str):

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        scan = update_scan_state(scan_id, ScanState.QUEUED)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    if not scan:
        return JsonResponse({"error": "Scan not found"}, status=404)

    return JsonResponse(scan)

from django.http import JsonResponse
from scans.repository import get_database


def scan_findings_view(request, scan_id: str):
    """
    Returns all findings for a given scan.
    Read-only.
    """
    if request.method != "GET":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    db = get_database()

    findings = list(
        db.findings.find(
            {"scan_id": scan_id},
            {"_id": 0},
        )
    )

    payload = {
        "scan_id": scan_id,
        "count": len(findings),
        "findings": findings,
    }

    validated = FindingsResponseSchema(**payload)

    return JsonResponse(
        validated.model_dump(),
        status=200,
    )
    
from scans.summary import build_scan_summary


def scan_summary_view(request, scan_id: str):
    """
    Returns aggregated summary for a scan.
    Read-only.
    """
    if request.method != "GET":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    summary = build_scan_summary(scan_id)

    validated = ScanSummarySchema(**summary)

    return JsonResponse(
        validated.model_dump(),
        status=200,
    )

