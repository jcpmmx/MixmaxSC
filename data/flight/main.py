# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

import requests

from django.conf import settings

from data.flight.utils import is_flight_code

_FLIGHTAWARE_BASE_URL = 'https://flightxml.flightaware.com/json/FlightXML3'
_FLIGHTAWARE_AUTH = (settings.FLIGHTAWARE_USERNAME, settings.FLIGHTAWARE_API_KEY)


def get_flight_data(flight_code):
    """
    Returns all flight data found for the given flight code using FlightInfoStatus method from FlightAware API.

    Full documentation: https://flightaware.com/commercial/flightxml/v3/apiref.rvt#op_FlightInfoStatus
    """
    if not is_flight_code(flight_code):
        return

    url = '{}/{}'.format(_FLIGHTAWARE_BASE_URL, 'FlightInfoStatus')
    data = {'ident': flight_code.upper(), 'howMany': 3}
    response = requests.get(url, data, auth=_FLIGHTAWARE_AUTH)
    if response.ok:
        response_data = response.json()
        if 'FlightInfoStatusResult' in response_data:
            flight_data = response_data['FlightInfoStatusResult']['flights']
            return sorted(flight_data, key=lambda x: x['filed_departure_time'])
