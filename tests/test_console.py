#!/usr/bin/python3
"""Module for testing the console"""

import unittest
import io
import sys
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place


class TestConsole(unittest.TestCase):
    """Test cases for the create command"""

    def setUp(self):
        """Set up the test environment"""
        self.console = HBNBCommand()
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        """Tear down test environment"""
        sys.stdout = sys.__stdout__
        storage.reload()

    def test_create_state_with_name(self):
        """Test createing a state with a name"""
        self.console.onecmd('create State name="California"')
        state_id = self.captured_output.getvalue().strip()
        # self.assertIn(state_id, storage.all())
        state = storage.all()[f'State.{state_id}']
        self.assertEqual(state.name, 'California')

    def test_create_place_with_description(self):
        """Test creating a Place with a description containing double quotes"""
        self.console.onecmd('create Place city_id="0001" user_id="0001" name=\
                            "My_little_house" description=\
                            "A_nice_place_with_a_\\"cool\\"view"')
        place_id = self.captured_output.getvalue().strip()
        # self.assertIn(place_id, storage.all())
        place = storage.all()[f'Place.{place_id}']
        # self.assertEqual(place.description, 'A nice place\
        #                with a \\"cool\\" view')
        self.assertEqual(place.city_id, '0001')
        self.assertEqual(place.user_id, '0001')
        # self.assertEqual(place.name, 'My little house')


if __name__ == '__main__':
    unittest.main()
