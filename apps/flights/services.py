import requests

from datetime import datetime, timedelta
from typing import List, Dict

from django.conf import settings

from apps.flights.exceptions import FlightNotFoundError, FlightEventNotFoundError
from apps.flights.models import City, Flight, FlightEvent


class FlightEventExternalService:
    def __init__(self):
        self.base_url = settings.FLIGHT_EVENTS_URL
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_flight_events(self) -> List[Dict]:
        response = requests.get(self.base_url, headers=self.headers)  # NOTE: not working
        response.raise_for_status()
        data = response.json()

        return data


class FlightEventService:

    FlightEventNotFoundError = FlightEventNotFoundError

    def __init__(self, from_city: City, to_city: City, departure_on: datetime):
        self.from_city = from_city
        self.to_city = to_city
        self.departure_on = departure_on

    def get_flight_events(self) -> List[Dict]:
        try:
            flight_events = FlightEvent.get_flight_events(self.from_city, self.to_city, self.departure_on)
        except (Flight.DoesNotExist, FlightEvent.DoesNotExist):
            raise self.FlightEventNotFoundError

        return flight_events
