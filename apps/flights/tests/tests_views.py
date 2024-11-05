from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.flights.models import City, Flight, FlightEvent


class FlightTestCase(APITestCase):

    def setUp(self):
        # self.client = APIClient()
        self.url = "/api/v1/journeys/search/"

        self.in_5_days = timezone.now() + timedelta(days=5)
        self.in_5_days_and_12_hs = self.in_5_days + timedelta(hours=12)

        self.bue = City.objects.create(code="BUE", name="Buenos Aires")
        self.mad = City.objects.create(code="MAD", name="Madrid")
        self.pdm = City.objects.create(code="PDM", name="Palma de Mallorca")

        self.xx1234 = Flight.objects.create(code="XX1234", from_city=self.bue, to_city=self.mad)
        self.yy1234 = Flight.objects.create(code="YY1234", from_city=self.bue, to_city=self.pdm)
        self.bb1234 = Flight.objects.create(code="BB1234", from_city=self.mad, to_city=self.pdm)

        self.bue_pdm = FlightEvent.objects.create(flight=self.yy1234, departure_on=self.in_5_days, arrival_on=self.in_5_days_and_12_hs + timedelta(hours=2))
        self.bue_mad = FlightEvent.objects.create(flight=self.xx1234, departure_on=self.in_5_days, arrival_on=self.in_5_days_and_12_hs)
        self.mad_pdm = FlightEvent.objects.create(flight=self.bb1234, departure_on=self.in_5_days_and_12_hs + timedelta(minutes=30), arrival_on=self.in_5_days_and_12_hs + timedelta(hours=2))

    def test_journey_search(self):
        """ Test BUE (Buenos Aires) to PDM (Palma de Mallorca) flights """

        date = self.in_5_days.date().isoformat()
        params = {"from": self.bue.code, "to": self.pdm.code, "date": date}
        response = self.client.get(self.url, params, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        # test direct flights
        self.assertEquals(response_data[0]["connections"], 1)
        self.assertEquals(response_data[0]["path"][0]["flight_number"], self.bue_pdm.flight.code)
        self.assertEquals(response_data[0]["path"][0]["from_city"], self.bue_pdm.flight.from_city.code)
        self.assertEquals(response_data[0]["path"][0]["to_city"], self.bue_pdm.flight.to_city.code)
        self.assertEquals(response_data[0]["path"][0]["departure_time"], self.bue_pdm.departure_on.strftime("%Y-%m-%d %H:%M"))
        self.assertEquals(response_data[0]["path"][0]["arrival_time"], self.bue_pdm.arrival_on.strftime("%Y-%m-%d %H:%M"))

        # test connection flights
        self.assertEquals(response_data[1]["connections"], 2)
        self.assertEquals(response_data[1]["path"][0]["flight_number"], self.bue_mad.flight.code)
        self.assertEquals(response_data[1]["path"][0]["from_city"], self.bue_mad.flight.from_city.code)
        self.assertEquals(response_data[1]["path"][0]["to_city"], self.bue_mad.flight.to_city.code)
        self.assertEquals(response_data[1]["path"][0]["departure_time"], self.bue_mad.departure_on.strftime("%Y-%m-%d %H:%M"))
        self.assertEquals(response_data[1]["path"][0]["arrival_time"], self.bue_mad.arrival_on.strftime("%Y-%m-%d %H:%M"))

        self.assertEquals(response_data[1]["path"][1]["flight_number"], self.mad_pdm.flight.code)
        self.assertEquals(response_data[1]["path"][1]["from_city"], self.mad_pdm.flight.from_city.code)
        self.assertEquals(response_data[1]["path"][1]["to_city"], self.mad_pdm.flight.to_city.code)
        self.assertEquals(response_data[1]["path"][1]["departure_time"], self.mad_pdm.departure_on.strftime("%Y-%m-%d %H:%M"))
        self.assertEquals(response_data[1]["path"][1]["arrival_time"], self.mad_pdm.arrival_on.strftime("%Y-%m-%d %H:%M"))
