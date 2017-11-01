# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals


def is_flight_code(flight_code):
    """
    Small stupid method that guesses if the given string represents a flight code or not.
    """
    # TODO(Julian): Add a regex check
    return len(flight_code) > 2
