from datetime import datetime, timedelta
from typing import List, Dict

from django.conf import settings
from django.db import models
from django.db.models import F
from django.utils import timezone

from apps.flights.exceptions import FlightNotFoundError, FlightEventNotFoundError


class City(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @classmethod
    def get_city_by_code(cls, code: str, raise_exc: bool = False) -> "City":
        city = cls.objects.filter(code=code).last()

        if not city and raise_exc:
            raise cls.DoesNotExist

        return city


class Flight(models.Model):
    from_city = models.ForeignKey(City, on_delete=models.DO_NOTHING, related_name="flights_from")
    to_city = models.ForeignKey(City, on_delete=models.DO_NOTHING, related_name="flights_to")
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return self.code

    @classmethod
    def get_direct_flights(cls, from_city: City, to_city: City, raise_exc: bool = True) -> List["Flight"]:
        flights = cls.objects.select_related("from_city", "to_city").filter(from_city=from_city, to_city=to_city)

        if not flights and raise_exc:
            raise cls.DoesNotExist

        return flights


class FlightEvent(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.DO_NOTHING)
    departure_on = models.DateTimeField()
    arrival_on = models.DateTimeField()

    def __str__(self):
        return f"{self.flight} - {self.departure_on}"
    
    @classmethod
    def get_flight_events(cls, from_city: City, to_city: City, departure_on: datetime, raise_exc: bool = True) -> List[Dict]:
        _flight_events = FlightEvent.objects.select_related("flight")

        direct_flights = Flight.get_direct_flights(from_city, to_city)
        direct_flights_events = _flight_events.filter(flight__in=direct_flights, departure_on__date=departure_on)

        first_connection_flights = _flight_events.filter(
            flight__from_city=from_city,
            departure_on__date=departure_on
        ).exclude(flight__in=direct_flights)

        connection_flight_events = []
        for first_flight in first_connection_flights:
            second_connection_flights = _flight_events.filter(
                flight__from_city=first_flight.flight.to_city,
                flight__to_city=to_city,
                departure_on__gte=first_flight.arrival_on + timedelta(minutes=settings.FLIGHT_MIN_CONNECTION_TIME),
                departure_on__lte=first_flight.arrival_on + timedelta(hours=settings.FLIGHT_MAX_CONNECTION_TIME)
            )

            for second_flight in second_connection_flights:
                if second_flight.arrival_on > first_flight.departure_on + timedelta(hours=settings.FLIGHT_MAX_DURATION_TIME):
                    continue  # discard due max time

                connection_flight_events.append({
                    "first_connection": first_flight,
                    "second_connection": second_flight
                })

        if not connection_flight_events and raise_exc:
            raise cls.DoesNotExist
        
        flight_events = []
        for direct_flight in direct_flights_events:
            flight_event = {
                "connections": 1,
                "path": [
                    {
                        "flight_number": direct_flight.flight.code,
                        "from_city": direct_flight.flight.from_city.code,
                        "to_city": direct_flight.flight.to_city.code,
                        "departure_time": direct_flight.departure_on,
                        "arrival_time": direct_flight.arrival_on,
                    }
                ]
            }
            flight_events.append(flight_event)

        for connection_flight in connection_flight_events:
            flight_event = {
                "connections": 2,
                "path": [
                    {
                        "flight_number": connection_flight["first_connection"].flight.code,
                        "from_city": connection_flight["first_connection"].flight.from_city.code,
                        "to_city": connection_flight["first_connection"].flight.to_city.code,
                        "departure_time": connection_flight["first_connection"].departure_on,
                        "arrival_time": connection_flight["first_connection"].arrival_on,
                    },
                    {
                        "flight_number": connection_flight["second_connection"].flight.code,
                        "from_city": connection_flight["second_connection"].flight.from_city.code,
                        "to_city": connection_flight["second_connection"].flight.to_city.code,
                        "departure_time": connection_flight["second_connection"].departure_on,
                        "arrival_time": connection_flight["second_connection"].arrival_on,
                    }
                ]
            }
            flight_events.append(flight_event)

        return flight_events
