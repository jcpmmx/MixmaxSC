# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from rest_framework import serializers

from computer.models import Computer
from computer.enums import ComputerInstruction


class ComputerSerializer(serializers.ModelSerializer):
    """
    Serializer to manage `Computer` instances.
    """
    stack = serializers.IntegerField(label='stack', write_only=True, help_text="Size of the computer's program stack.")
    debug_data = serializers.DictField(read_only=True, source='debug')

    class Meta:
        model = Computer
        fields = ('id', 'stack', 'debug_data')

    def create(self, validated_data):
        """
        Creates a new `Computer` instance via API.
        """
        validated_data['program_stack_size'] = validated_data.pop('stack', 0)
        return super(ComputerSerializer, self).create(validated_data)


class ComputerPointerSerializer(serializers.Serializer):
    """
    Serializer to manage arguments passed to `Computer` pointer.
    """
    addr = serializers.IntegerField(
        label='addr', write_only=True, help_text='The address to set the program stack pointer to.')


class ComputerInsertSerializer(serializers.Serializer):
    """
    Serializer to manage arguments passed to `Computer` instructions.
    """
    arg = serializers.IntegerField(label='arg', write_only=True, default=None, help_text='Required when using PUSH.')
    addr = serializers.IntegerField(label='addr', write_only=True, default=None, help_text='Required when using CALL.')

    def validate_arg(self, value):
        if self.context['instruction'] == ComputerInstruction.PUSH and not value:
            raise serializers.ValidationError('You must provide this value when using PUSH.')
        return value

    def validate_addr(self, value):
        if self.context['instruction'] == ComputerInstruction.CALL and not value:
            raise serializers.ValidationError('You must provide this value when using CALL.')
        return value

    def validate(self, data):
        if self.context['instruction'] == ComputerInstruction.CALL:
            data['arg'] = data.pop('addr')
        return data
