from django.urls import path
from api.views import list_profiles, get_profile

urlpatterns = [
    path("profiles/", list_profiles),
    path("profiles/<str:name>/", get_profile),
]

from api.views import create_scan_view

urlpatterns += [
    path("scans/", create_scan_view),
]

from api.views import list_scans_view, get_scan_view

urlpatterns += [
    path("scans/", list_scans_view),
    path("scans/<str:scan_id>/", get_scan_view),
]
