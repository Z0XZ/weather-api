from django.urls import path
from .views import SensorDataView
from . import views

urlpatterns = [
    path("sensor-data/", SensorDataView.as_view(), name="sensor-data"),
    path("sensor-data/plot/", views.plot_data_json, name="plot-data"),
    path("sensor-data/export.csv", views.export_csv, name="export-csv"),
]
