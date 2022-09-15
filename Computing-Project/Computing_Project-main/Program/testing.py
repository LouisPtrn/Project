# ============================================================================================================== #
# This file is used for unit testing
# Written by: Louis Pattern     10/09/2022
# Known bugs: none
# ============================================================================================================== #

import unittest
from settings import *


class TestMethods(unittest.TestCase):
    # Tests a setting that doesn't exist
    def test_invalid_setting(self):
        self.assertEqual(get_setting("Non-existent setting"), "Setting not found")

    # Testing saving and loading existent settings
    def test_valid_setting(self):
        save_setting("difficulty", "Easy")
        self.assertEqual(get_setting("difficulty"), "Easy")

        save_setting("difficulty", "Normal")
        self.assertEqual(get_setting("difficulty"), "Normal")

    def test_colour(self):
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

    def test_error(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
