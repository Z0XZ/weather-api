from django.utils import timezone
from datetime import datetime, timedelta
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

def voltage_to_percent(voltage):
    if voltage is None:
        return None
    if voltage >= 4.20: return 100
    if voltage >= 4.15: return 95
    if voltage >= 4.10: return 90
    if voltage >= 4.00: return 80
    if voltage >= 3.90: return 70
    if voltage >= 3.80: return 60
    if voltage >= 3.70: return 50
    if voltage >= 3.60: return 30
    if voltage >= 3.50: return 15
    if voltage >= 3.40: return 5
    return 0

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
            battery_voltage = request.data.get("battery_voltage")
            battery_percent = voltage_to_percent(float(battery_voltage)) if battery_voltage else None

            validated_data = serializer.validated_data
            validated_data["battery"] = battery_percent
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
    fields = ["temperature", "humidity", "pressure", "light"]
    units = {
        "temperature": "°C",
        "humidity": "%",
        "pressure": "Pa",
        "light": "",
    }
    field_labels = {
        "temperature": "Temperatur",
        "humidity": "Luftfuktighet",
        "pressure": "Trykk",
        "light": "Lys",
    }

    # Lag en liste med dictionaries som inneholder både felt og oversettelse
    field_data = [
        {
            "key": f,
            "label": field_labels[f],
            "unit": units[f],
        }
        for f in fields
    ]

    # Hent siste batteriverdier per location
    latest_fill = {}
    latest_battery = {}
    for location in ["Sandnes", "Stavanger"]:
        latest = SensorData.objects.filter(location__iexact=location).order_by("-timestamp").first()
        if latest and latest.battery is not None:
            battery_int = int(latest.battery)
            latest_battery[location] = battery_int
            latest_fill[location] = int((battery_int / 100) * 18)  # batterifyll bredde i px
        else:
            latest_battery[location] = 0
            latest_fill[location] = 0

    return render(
        request,
        "sensors/dashboard.html",
        {
            "locations": ["Sandnes", "Stavanger"],
            "field_data": field_data,  # send liste med både key og label
            "latest_battery": latest_battery,
            "latest_fill": latest_fill,
        },
    )


from datetime import datetime

def plot_data_json(request):
    esp_id = request.GET.get("esp_id")
    field = request.GET.get("field")
    location = request.GET.get("location")
    range_param = request.GET.get("range")
    start = request.GET.get("start")
    end = request.GET.get("end")

    if not esp_id or not field:
        return JsonResponse({"error": "esp_id og field må være angitt"}, status=400)

    data = SensorData.objects.filter(esp_id=esp_id)
    if location:
        data = data.filter(location__iexact=location)

    # Forhåndsdefinerte intervaller
    if range_param == "day":
        data = data.filter(timestamp__date=timezone.now().date())
    elif range_param == "month":
        now = timezone.now()
        data = data.filter(timestamp__year=now.year, timestamp__month=now.month)
    elif range_param == "year":
        data = data.filter(timestamp__year=timezone.now().year)

    # Egendefinert periode
    if start:
        try:
            start_dt = datetime.strptime(start, "%Y-%m-%d")
            data = data.filter(timestamp__gte=start_dt)
        except ValueError:
            pass

    if end:
        try:
            end_dt = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
            data = data.filter(timestamp__lt=end_dt)
        except ValueError:
            pass

    data = data.order_by("-timestamp")
    data = reversed(data)

    datapoints = []
    for d in data:
        value = getattr(d, field, None)
        if value is not None:
            datapoints.append({"x": d.timestamp.isoformat(), "y": float(value)})

    return JsonResponse({"data": datapoints})


def export_csv(request):
    esp_id = request.GET.get("esp_id")
    field = request.GET.get("field")
    location = request.GET.get("location")

    data = SensorData.objects.all()
    if esp_id:
        data = data.filter(esp_id=esp_id)
    if location:
        data = data.filter(location__iexact=location)
    
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
                [
                    d.timestamp,
                    d.location,
                    d.temperature,
                    d.humidity,
                    d.pressure,
                    d.light,
                ]
            )

    return response
