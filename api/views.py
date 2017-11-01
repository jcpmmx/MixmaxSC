# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from datetime import datetime

from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django.core.cache import cache
from django.template.loader import render_to_string

from data.flight.main import get_flight_data
from data.flight.utils import is_flight_code


class FlightCommandViewset(GenericViewSet):
    """
    API views available to use the `flight` slash command.
    """

    @list_route(methods=['get'])
    def suggestions(self, request):
        """
        Returns all suggestions for the `flight` slash command using the given data from Mixmax client.
        """
        # TODO(Julian): Implement this with serializers
        flight_code = request.query_params.get('text', '')
        if is_flight_code(flight_code):
            return Response(self._parse_suggestions(get_flight_data(flight_code)))

        return Response([{'title': 'No flight data found', 'text': 'No results found'}])

    @list_route(methods=['get'])
    def resolver(self, request):
        """
        Returns the resolved HTML widget for the chosen suggestion for the `flight` slash command using the given data
        from Mixmax client.
        """
        # TODO(Julian): Implement this with serializers
        flight_id = request.query_params.get('text', '')
        if flight_id:
            return Response(self._parse_resolver(flight_id))

        return Response(
            {'message': "Flight data could't be parsed, please try again"},
            status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def _parse_suggestions(cls, flight_data):
        """
        Parses flight data (as returned by FlightAware API) and parses for the command suggestions (as expected by
        Mixmax client).

        Documentation on the expected format by Mixmax: https://developer.mixmax.com/v1.0/docs/overview-slash-commands
        """
        if flight_data:
            suggestions = []

            for flight in flight_data:

                # Creating the suggestion
                friendly_ts = cls._get_friendly_ts(flight['filed_departure_time']['localtime'])
                new_suggestion = {
                    'title': '{flight_code} - {origin} to {destination} ({ts})'.format(
                        flight_code=flight['ident'],
                        origin=flight['origin']['city'],
                        destination=flight['destination']['city'],
                        ts=friendly_ts),
                    'text': '{}'.format(flight['faFlightID']),
                }
                suggestions.append(new_suggestion)

                # Adding flight data to cache in case this suggestion gets picked
                cache.set(flight['faFlightID'], flight)

            return suggestions

    @classmethod
    def _parse_resolver(cls, flight_id):
        """
        Parses flight data (as returned by FlightAware API) and parses for the command resolver (as expected by Mixmax
        client).

        Documentation on the expected format by Mixmax: https://developer.mixmax.com/v1.0/docs/overview-slash-commands
        """
        flight_data = cache.get(flight_id)
        if not flight_data:
            return

        context = {
            'flight_code': flight_data['ident'],
            'status': flight_data['status'],
            'origin': flight_data['origin']['city'],
            'destination': flight_data['destination']['city'],
            'departure_ts': cls._get_friendly_ts(flight_data['filed_departure_time']['localtime']),
            'arrival_ts': cls._get_friendly_ts(flight_data['filed_arrival_time']['localtime']),
            'origin_airport': flight_data['origin']['airport_name'],
            'destination_airport': flight_data['destination']['airport_name'],
            'duration': cls._seconds_to_ts(flight_data['filed_ete']),
        }
        return {'body': render_to_string('resolver.html', context)}

    @staticmethod
    def _get_friendly_ts(timestamp_int):
        """
        Takes an int representing a datetime (in local time) and returns a friendly timestamp for it.
        e.g. Nov 13 07:33 PM
        """
        return datetime.fromtimestamp(timestamp_int).strftime('%b %d %I:%M %p')

    @staticmethod
    def _seconds_to_ts(seconds):
        """
        Takes an int representing a given amount of seconds and returns a friendly timestamp for it.
        e.g. 7700 > "02:08:20"
        """
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return '%d:%02d' % (hours, minutes)
