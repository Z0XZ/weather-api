from django.contrib import admin
from .models import SensorData


# Register your models here.
@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "esp_id",
        "location",
        "temperature",
        "humidity",
        "pressure",
        "light",
        "timestamp",
        "battery",
        "battery_voltage",
    )  # Add all the fields you want to see in the list view

    # Controls the fields displayed when editing/creating a Group (form view)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "esp_id",
                    "temperature",
                    "location",
                    "humidity",
                    "pressure",
                    "light",
                    "battery",
                    "battery_voltage"
                )  # Add all fields you want in the form
            },
        ),
    )
