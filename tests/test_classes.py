import unittest
from classes import *
from functions import *
from main import *


class TestShow(unittest.TestCase):
    def test_add_event(self):
        # Test adding a new movie
        Show.add_show(1, '19:00:00', '22:00:00', 200,  '01/10/2022')
        self.assertIn( 1, [show['show_id'] for show in get_list_from_json()

        # Test adding an existing movie
        with self.assertRaises(ValueError):
            Show.add_show(1, '19:00:00', '22:00:00', 200,  '01/10/2022')

    def test_edit_event(self):
        # Test editing an existing movie
        show = Show.get_list_from_json()['1']
        Show.edit_show('1', '2','18:30:00' , '21:30:00', 150, '02/10/2022')
        edited_show = Show.get_list_from_json()['1']
        self.assertNotEqual(show['show_id'], edited_show['show_id'])
        self.assertEqual(edited_show['show_id'], '1')
        self.assertEqual(edited_show['event_id'], '2')
        self.assertEqual(edited_show['start_time'], '18:30:00')
        self.assertEqual(edited_show['end_time'], '21:30:00')
        self.assertEqual(edited_show['price'], 150)
        self.assertEqual(edited_show['datetime'], '02/10/2022')
        # Test editing a non-existing movie
        with self.assertRaises(KeyError):
            Show.edit_show('1', '2','18:30:00' , '21:30:00', 150, '02/10/2022')

    def test_delete_show(self):
        # Test deleting an existing movie
        Show.delete_show('1')
        self.assertNotIn('1', Show.get_list_from_json().keys())

        # Test deleting a non-existing movie
        with self.assertRaises(KeyError):
            Show.delete_show('1')



