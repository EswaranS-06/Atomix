import os
from django.http import JsonResponse, Http404
from config.profiles.loader import load_profile, ProfileError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from scans.repository import create_scan
from config.profiles.loader import load_profile, ProfileError



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
