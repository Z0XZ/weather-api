from django.contrib import admin
from .models import SensorData


# Register your models here.
@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "esp_id",
        "temperature",
        "humidity",
        "pressure",
        "light",
        "created_at",
    )  # Add all the fields you want to see in the list view

    # Controls the fields displayed when editing/creating a Group (form view)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "esp_id",
                    "temperature",
                    "humidity",
                    "pressure",
                    "light",
                    "created_at",
                )  # Add all fields you want in the form
            },
        ),
    )
