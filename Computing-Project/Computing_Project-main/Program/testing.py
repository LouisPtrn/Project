# ============================================================================================================== #
# This file is used for unit testing
# Written by: Louis Pattern     11/09/2022
# Known bugs: none
# ============================================================================================================== #

import unittest
from settings import *

class TestMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual(get_setting("Non-existent setting"), "Setting not found")

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()