# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from rest_framework import mixins, status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from api.serializers import ComputerInsertSerializer, ComputerPointerSerializer, ComputerSerializer


class FlightCommandViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    API view to manage `Computer` instances.

    create:
    Creates a new `Computer` with the given stack size.

    retrieve:
    Returns all data about the `Computer` with the given ID.
    """
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer

    @detail_route(
        methods=['patch'], serializer_class=ComputerPointerSerializer, url_path='stack/pointer', url_name='pointer')
    def pointer(self, request, pk=None):
        """
        Sets the address of the program stack of a `Computer`.
        """
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        computer = self.get_object()
        computer.set_address(serializer.validated_data['addr'], save=True)
        return Response(computer.debug())

    @detail_route(
        methods=['post'], serializer_class=ComputerInsertSerializer,
        url_path='stack/insert/(?P<possible_instruction>[^/.]+)', url_name='insert')
    def insert(self, request, pk=None, possible_instruction=None):
        """
        Inserts the given instruction, with its optional argument, in a `Computer`.
        """
        instruction = ComputerInstruction.get_value(possible_instruction)
        if instruction:
            serializer = self.get_serializer_class()(data=request.data, context={'instruction': instruction})
            serializer.is_valid(raise_exception=True)
            computer = self.get_object()
            computer.insert(instruction, instruction_arg=serializer.validated_data['arg'], save=True)
            return Response(computer.debug())
        return Response({'detail': 'You must provide a valid instruction'}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], serializer_class=Serializer, url_path='exec', url_name='execute')
    def execute(self, request, pk=None):
        """
        Executes the current program of a `Computer`.
        """
        computer = self.get_object()
        try:
            program_output = computer.execute()
            return Response({'program_output': program_output})
        except Exception, e:
            raise APIException("Unexpected error when executing the program: {}".format(e))

    @detail_route(methods=['post'], serializer_class=Serializer, url_path='debug')
    def debug(self, request, pk=None):
        """
        Returns all debug data from a `Computer`.
        """
        computer = self.get_object()
        return Response(computer.debug())
