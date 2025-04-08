from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SensorData
from .serializers import SensorDataSerializer
import csv

# Din hemmelige API-nøkkel for ESP
AUTHORIZED_KEYS = {"esp32-a1b2c3": "abc123esp", "esp32-x9y8z7": "xyz456esp"}


class SensorDataView(APIView):
    def post(self, request):
        esp_id = request.data.get("esp_id")
        api_key = request.headers.get("X-API-KEY")

        # Sjekk at esp_id og nøkkel matcher
        if not esp_id or api_key != AUTHORIZED_KEYS.get(esp_id):
            return Response(
                {"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data lagret"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        esp_id = request.query_params.get("esp_id", None)
        if esp_id:
            data = SensorData.objects.filter(esp_id=esp_id).order_by("-timestamp")
        else:
            data = SensorData.objects.order_by("-timestamp")
        serializer = SensorDataSerializer(data, many=True)
        return Response(serializer.data)


def dashboard_view(request):
    return render(request, "sensors/dashboard.html")


def plot_data_json(request):
    esp_id = request.GET.get("esp_id")
    field = request.GET.get("field")

    if not esp_id or not field:
        return JsonResponse({"error": "esp_id og field må være angitt"}, status=400)

    data = SensorData.objects.filter(esp_id=esp_id).order_by("-timestamp")[:50]
    data = reversed(data)  # sorterer i riktig rekkefølge

    datapoints = []
    for d in data:
        value = getattr(d, field, None)
        if value is not None:
            datapoints.append(
                {
                    "x": d.timestamp.isoformat(),
                    "y": float(value),
                }
            )

    return JsonResponse({"data": datapoints})


def export_csv(request):
    esp_id = request.GET.get("esp_id")
    field = request.GET.get("field")

    data = SensorData.objects.all()
    if esp_id:
        data = data.filter(esp_id=esp_id)
    if field:
        header = ["timestamp", field]
    else:
        header = [
            "timestamp",
            "location",
            "temperature",
            "humidity",
            "pressure",
            "light",
        ]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="sensor_data.csv"'

    writer = csv.writer(response)
    writer.writerow(header)

    for d in data:
        if field:
            writer.writerow([d.timestamp, getattr(d, field)])
        else:
            writer.writerow(
                [d.timestamp, d.temperature, d.humidity, d.pressure, d.light]
            )

    return response
