from django.http import JsonResponse
from scans.apps import ScanState


def health_check(request):
    return JsonResponse(
        {
            "status": "ok",
            "project": "ATOMIX",
            "phase": "Phase 1",
            "scan_states": sorted(list(ScanState.ALL)),
        }
    )
