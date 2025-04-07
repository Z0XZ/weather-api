from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SensorData
from .serializers import SensorDataSerializer

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
            data = SensorData.objects.filter(esp_id=esp_id).order_by("-created_at")
        else:
            data = SensorData.objects.order_by("-created_at")
        serializer = SensorDataSerializer(data, many=True)
        return Response(serializer.data)
