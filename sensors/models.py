from django.db import models


class SensorData(models.Model):
    esp_id = models.CharField(max_length=100)  # F.eks. MAC-adresse eller unik ID
    temperature = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    light = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} - {self.esp_id} - {self.temperature}°C"
