from django.db import models


class SensorData(models.Model):
    esp_id = models.CharField(max_length=100)  # F.eks. MAC-adresse eller unik ID
    location = models.CharField(max_length=100)  # By
    temperature = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    light = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    battery = models.IntegerField(null=True, blank=True) #Batteriprosent
    battery_voltage = models.FloatField(null=True, blank=True)  # Målt spenning i volt
    wind_freq = models.FloatField(null=True, blank=True, help_text="Frekvens fra vindmåler (Hz)")
    wind_speed = models.FloatField(null=True, blank=True, help_text="Vindhastighet beregnet fra frekvens (m/s)")

    def __str__(self):
        return f"{self.timestamp} - {self.esp_id} - {self.temperature}°C"
