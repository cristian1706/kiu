from django.urls import path

from apps.flights.views import FlightView


app_name = "flights"

urlpatterns = [
    path("journeys/search/", FlightView.as_view(), name="journeys-search"),
]
