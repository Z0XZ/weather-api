from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from sensors import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("sensors.urls")),
    path("dashboard/", views.dashboard_view, name="dashboard"),
]

# Kun for utvikling (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)