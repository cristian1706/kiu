from datetime import datetime

from rest_framework import status, serializers

from apps.flights.constants import FlightErrorCode
from apps.flights.models import City


class FlightEventInputSerializer(serializers.Serializer):

    from_city = serializers.CharField(max_length=3)
    to_city = serializers.CharField(max_length=3)
    departure_on = serializers.DateField(format="%Y-%m-%d")

    def to_internal_value(self, data):
        data["from_city"] = data.get("from")
        data["to_city"] = data.get("to")
        data["departure_on"] = data.get("date")
        return super().to_internal_value(data)

    def validate_from_city(self, city):
        city = City.get_city_by_code(city)
        if not city:
            raise serializers.ValidationError({"detail": "Origin city not found", "error_code": FlightErrorCode.FLIGHT_CITY_NOT_FOUND_ERROR.value}, status.HTTP_400_BAD_REQUEST)
        return city
    
    def validate_to_city(self, city):
        city = City.get_city_by_code(city)
        if not city:
            raise serializers.ValidationError({"detail": "Destiny city not found", "error_code": FlightErrorCode.FLIGHT_CITY_NOT_FOUND_ERROR.value}, status.HTTP_400_BAD_REQUEST)
        return city

    def validate_departure_on(self, departure_on):
        # far dates can also be filtered
        if departure_on < datetime.today().date():
            raise serializers.ValidationError({"detail": "The date must be greather than today", "error_code": FlightErrorCode.FLIGHT_DATE_ERROR.value}, status.HTTP_400_BAD_REQUEST)
        return departure_on
    

class FlightEventPathSerializer(serializers.Serializer):
    flight_number = serializers.CharField()
    from_city = serializers.CharField()
    to_city = serializers.CharField()
    departure_time = serializers.SerializerMethodField()
    arrival_time = serializers.SerializerMethodField()

    def get_departure_time(self, data):
        data["departure_time"] = data.pop("departure_time").strftime("%Y-%m-%d %H:%M")
        return data["departure_time"]

    def get_arrival_time(self, data):
        data["arrival_time"] = data.pop("arrival_time").strftime("%Y-%m-%d %H:%M")
        return data["arrival_time"]


class FlightEventOutputSerializer(serializers.Serializer):

    connections = serializers.IntegerField()
    path = FlightEventPathSerializer(many=True)
