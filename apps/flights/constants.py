from enum import Enum


class FlightErrorCode(Enum):
    """ Flight error codes starts with FLG_**** """

    FLIGHT_CONFLICT_ERROR = "FLG_0100"
    FLIGHT_NOT_FOUND_ERROR = "FLG_0200"
    FLIGHT_CITY_NOT_FOUND_ERROR = "FLG_0300"
    FLIGHT_DATE_ERROR = "FLG_0400"
