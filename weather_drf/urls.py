from django.contrib import admin
from django.urls import path, include
from sensors import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("sensors.urls")),
    path("dashboard/", views.dashboard_view, name="dashboard"),
]
