# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from django.core.urlresolvers import reverse


class FlightCommandAPITestCase(APITestCase):
    """
    Test case that check the behavior of the Computer API.

    All tests here are deliberately similar to the ones in `Computer` so we know both API and the model directly behave
    the same.
    """
    def setUp(self):
        self.api = APIClient()
        self.computers_url = reverse('computer-list')
        self.computer_pointer_url = lambda computer_id: reverse('computer-pointer', kwargs={'pk': computer_id})
        self.computer_insert = lambda computer_id, possible_instruction: reverse(
            'computer-insert', kwargs={'pk': computer_id, 'possible_instruction': possible_instruction})
        self.computer_execute = lambda computer_id: reverse('computer-execute', kwargs={'pk': computer_id})
        self.computer_debug = lambda computer_id: reverse('computer-debug', kwargs={'pk': computer_id})

    def test_good_program(self):
        """
        The program is as given originally by the test description and produces the expected output.
        """
        PRINT_TENTEN_BEGIN = 50
        MAIN_BEGIN = 0
        response = self.api.post(self.computers_url, {'stack': 100})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        computer_id = response.data['id']
        self.api.patch(self.computer_pointer_url(computer_id), {'addr': PRINT_TENTEN_BEGIN})
        self.api.post(self.computer_insert(computer_id, 'MULT'))
        self.api.post(self.computer_insert(computer_id, 'PRINT'))
        self.api.post(self.computer_insert(computer_id, 'RET'))
        self.api.patch(self.computer_pointer_url(computer_id), {'addr': MAIN_BEGIN})
        self.api.post(self.computer_insert(computer_id, 'PUSH'), {'arg': 1009})
        self.api.post(self.computer_insert(computer_id, 'PRINT'))
        self.api.post(self.computer_insert(computer_id, 'PUSH'), {'arg': 6})
        self.api.post(self.computer_insert(computer_id, 'PUSH'), {'arg': 101})
        self.api.post(self.computer_insert(computer_id, 'PUSH'), {'arg': 10})
        self.api.post(self.computer_insert(computer_id, 'CALL'), {'addr': PRINT_TENTEN_BEGIN})
        self.api.post(self.computer_insert(computer_id, 'STOP'))
        self.api.patch(self.computer_pointer_url(computer_id), {'addr': MAIN_BEGIN})
        response = self.api.post(self.computer_execute(computer_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        program_output_data = response.data['program_output']
        self.assertEqual(program_output_data, [1009, 1010])

    def test_bad_program(self):
        """
        We explicitly remove the STOP instruction, making the program enter an infinite loop that causes a failure when
        trying to execute MULT (line 50) without data in memory (since it has been already removed by the 1st run).
        """
        PRINT_TENTEN_BEGIN = 50
        MAIN_BEGIN = 0
        response = self.api.post(self.computers_url, {'stack': 100})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        computer_id = response.data['id']
        self.api.patch(self.computer_pointer_url(computer_id), {'addr': PRINT_TENTEN_BEGIN})
        self.api.post(self.computer_insert(computer_id, 'MULT'))
        self.api.post(self.computer_insert(computer_id, 'PRINT'))
        self.api.post(self.computer_insert(computer_id, 'RET'))
        self.api.patch(self.computer_pointer_url(computer_id), {'addr': MAIN_BEGIN})
        self.api.post(self.computer_insert(computer_id, 'PUSH'), {'arg': 1009})
        self.api.post(self.computer_insert(computer_id, 'PRINT'))
        self.api.post(self.computer_insert(computer_id, 'PUSH'), {'arg': 6})
        self.api.post(self.computer_insert(computer_id, 'PUSH'), {'arg': 101})
        self.api.post(self.computer_insert(computer_id, 'PUSH'), {'arg': 10})
        self.api.post(self.computer_insert(computer_id, 'CALL'), {'addr': PRINT_TENTEN_BEGIN})
        #self.api.post(self.computer_insert(computer_id, 'STOP'))
        self.api.patch(self.computer_pointer_url(computer_id), {'addr': MAIN_BEGIN})
        response = self.api.post(self.computer_execute(computer_id))
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('Unexpected error', response.data['detail'])

    def test_different_program(self):
        """
        We create a different program to make sure everything works as expected.
        """
        response = self.api.post(self.computers_url, {'stack': 30})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        computer_id = response.data['id']
        self.api.post(self.computer_insert(computer_id, 'PUSH'), {'arg': 7})
        self.api.post(self.computer_insert(computer_id, 'PUSH'), {'arg': 7})
        self.api.post(self.computer_insert(computer_id, 'PUSH'), {'arg': 49})
        self.api.post(self.computer_insert(computer_id, 'CALL'), {'addr': 13})
        self.api.patch(self.computer_pointer_url(computer_id), {'addr': 13})
        self.api.post(self.computer_insert(computer_id, 'PRINT'))
        self.api.post(self.computer_insert(computer_id, 'MULT'))
        self.api.post(self.computer_insert(computer_id, 'PRINT'))
        self.api.post(self.computer_insert(computer_id, 'STOP'))
        self.api.patch(self.computer_pointer_url(computer_id), {'addr': 0})
        response = self.api.post(self.computer_execute(computer_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        program_output_data = response.data['program_output']
        self.assertEqual(program_output_data, [49, 49])
