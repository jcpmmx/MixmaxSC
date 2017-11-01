# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from rest_framework.routers import DefaultRouter

from api.views import FlightCommandViewset

router = DefaultRouter()
router.register(r'computers', ComputerViewset)
