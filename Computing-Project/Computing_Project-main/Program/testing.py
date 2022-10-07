# ============================================================================================================== #
# This file is used for unit testing
# Written by: Louis Pattern     10/09/2022
# Known bugs: none
# ============================================================================================================== #

import unittest
from settings import *
from validation import *


class TestMethods(unittest.TestCase):
    # -----------------------------------------------------------------------------
    # TESTING SETTINGS
    def test_invalid_setting(self):  # Tests a setting that doesn't exist
        self.assertEqual(get_setting("Non-existent setting"), "Setting not found")

    def test_valid_setting(self):  # Testing saving and loading existent settings
        save_setting("difficulty", "Easy")
        self.assertEqual(get_setting("difficulty"), "Easy")

        save_setting("difficulty", "Normal")
        self.assertEqual(get_setting("difficulty"), "Normal")

    def test_colour(self):  # Testing saving and loading colour
        save_setting("colour", "True")
        data = (get_setting("colour"))
        if data == "True":
            data = 1
        else:
            data = 0
        self.assertTrue(data)

        save_setting("colour", "False")
        data = (get_setting("colour"))
        if data == "True":
            data = 1
        else:
            data = 0
        self.assertFalse(data)

    # -----------------------------------------------------------------------------
    # TESTING VALIDATION
    def test_scores(self):
        self.assertEqual(is_valid_score(1000), True)  # Valid score
        self.assertEqual(is_valid_score(-100), False)  # Invalid score
        self.assertEqual(is_valid_score(500.5), False)  # Invalid score
        self.assertEqual(is_valid_score(0), True)  # Borderline
        self.assertEqual(is_valid_score(999999), True)  # Borderline

    # testing dates dd/mm/yyyy format
    def test_dates(self):
        self.assertEqual(is_valid_date("01/01/2001"), True)  # Valid date
        self.assertEqual(is_valid_date("29/02/2004"), True)  # Valid date
        self.assertEqual(is_valid_date("40/10/1000"), False)  # Invalid date
        self.assertEqual(is_valid_date("31/09/2015"), False)  # Invalid date
        self.assertEqual(is_valid_date("30/12/9999"), True)  # Extreme

    # testing usernames
    def test_users(self):
        self.assertEqual(is_valid_user("Bob_12542", "username"), True)  # Valid username
        self.assertEqual(is_valid_user("L1", "username"), False)  # Invalid username, too short
        self.assertEqual(is_valid_user("qwertyuiop_asdfghjklzxc", "username"), False)  # Invalid username, too long
        self.assertEqual(is_valid_user("qwertyuiop_asgdhjlkl", "username"), True)  # Borderline
    # -----------------------------------------------------------------------------

    def test_error(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
