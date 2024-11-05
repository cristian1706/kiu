import logging

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.flights.constants import FlightErrorCode
from apps.flights.serializers import FlightEventInputSerializer, FlightEventOutputSerializer
from apps.flights.services import FlightEventService


class FlightView(APIView):
    permission_classes = [AllowAny]  # NOTE: no auth for challenge

    def get(self, request):
        params = request.query_params.copy()

        input_serializer = FlightEventInputSerializer(data=params)
        input_serializer.is_valid(raise_exception=True)

        from_city = input_serializer.validated_data["from_city"]
        to_city = input_serializer.validated_data["to_city"]
        departure_on = input_serializer.validated_data["departure_on"]

        try:
            service = FlightEventService(from_city, to_city, departure_on)
            flight_events = service.get_flight_events()

            output_serializer = FlightEventOutputSerializer(flight_events, many=True)
            return Response(output_serializer.data, status.HTTP_200_OK)
        except FlightEventService.FlightEventNotFoundError:
            return Response({"detail": "No journeys found for selected route and date", "error_code": FlightErrorCode.FLIGHT_NOT_FOUND_ERROR.value}, status.HTTP_404_NOT_FOUND)
        except Exception:
            logging.exception("FlightView: Could not get journeys")
            return Response({"detail": "Could not get journeys", "error_code": FlightErrorCode.FLIGHT_CONFLICT_ERROR.value}, status.HTTP_409_CONFLICT)
