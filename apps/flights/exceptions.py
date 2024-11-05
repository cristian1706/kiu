class FlightError(Exception):
    pass


class FlightNotFoundError(FlightError):
    pass


class FlightEventNotFoundError(FlightError):
    pass
