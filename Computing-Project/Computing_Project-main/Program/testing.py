# ============================================================================================================== #
# This file is used for unit testing modules and functions
# Written by: Louis Pattern     10/09/2022
# Known bugs: none
# ============================================================================================================== #

import unittest
from settings import *
from validation import *
from LoginData import *
from HighscoresData import *


# class TestMethods(unittest.TestCase):
    # # -----------------------------------------------------------------------------
    # # TESTING SETTINGS
    # def test_invalid_setting(self):  # Tests a setting that doesn't exist
    #     self.assertEqual(get_setting("Non-existent setting"), "Setting not found")
    #
    # def test_valid_setting(self):  # Testing saving and loading existent settings
    #     save_setting("difficulty", "Easy")
    #     self.assertEqual(get_setting("difficulty"), "Easy")
    #
    #     save_setting("difficulty", "Normal")
    #     self.assertEqual(get_setting("difficulty"), "Normal")
    #
    # def test_colour(self):  # Testing saving and loading colour
    #     save_setting("colour", "True")
    #     data = (get_setting("colour"))
    #     if data == "True":
    #         data = 1
    #     else:
    #         data = 0
    #     self.assertTrue(data)
    #
    #     save_setting("colour", "False")
    #     data = (get_setting("colour"))
    #     if data == "True":
    #         data = 1
    #     else:
    #         data = 0
    #     self.assertFalse(data)
    #
    # # -----------------------------------------------------------------------------
    # # TESTING VALIDATION
    # def test_scores(self):
    #     self.assertEqual(is_valid_score(1000), True)  # Valid score
    #     self.assertEqual(is_valid_score(-100), False)  # Invalid score
    #     self.assertEqual(is_valid_score(500.5), False)  # Invalid score
    #     self.assertEqual(is_valid_score(0), True)  # Borderline
    #     self.assertEqual(is_valid_score(999999), True)  # Borderline
    #
    # # testing dates dd/mm/yyyy format
    # def test_dates(self):
    #     self.assertEqual(is_valid_date("01/01/2001"), True)  # Valid date
    #     self.assertEqual(is_valid_date("29/02/2004"), True)  # Valid date
    #     self.assertEqual(is_valid_date("40/10/1000"), False)  # Invalid date
    #     self.assertEqual(is_valid_date("31/09/2015"), False)  # Invalid date
    #     self.assertEqual(is_valid_date("30/12/9999"), True)  # Extreme
    #
    # # testing usernames
    # def test_users(self):
    #     self.assertEqual(is_valid_user("Bob_12542", "username"), True)  # Valid username
    #     self.assertEqual(is_valid_user("L1", "username"), False)  # Invalid username, too short
    #     self.assertEqual(is_valid_user("qwertyuiop_asdfghjklzxc", "username"), False)  # Invalid username, too long
    #     self.assertEqual(is_valid_user("qwertyuiop_asgdhjlh", "username"), True)  # Borderline
    #
    # def test_passwords(self):
    #     self.assertEqual(is_valid_user("XQloP7*jsalHp!", "password"), True)  # Valid password
    #     self.assertEqual(is_valid_user("12345", "password"), False)  # Invalid Password
    #     self.assertEqual(is_valid_user(10000000000000, "password"), False)  # Invalid Password

    # -----------------------------------------------------------------------------
    # TESTING DB
    #
    # def test_existent_user(self):
    #     enter_user("LouisPattern13", "iloveunittesting")
    #     self.assertEqual(is_existent_user("LouisPattern13"), True)  # Existent user
    #     delete_user("LouisPattern13")
    #     self.assertEqual(is_existent_user("LouisPattern13"), False)  # Non-existent user
    #
    # def test_enter_user(self):
    #     self.assertEqual(enter_user("Inval", "bad"), False)  # Trying to enter invalid data
    #     self.assertEqual(enter_user("Valid_12345", "ComputerScience015"), True)  # Trying to enter valid data
    #     delete_user("Valid_12345")
    #
    # def test_enter_score(self):
    #     self.assertEqual(enter_score("User", -100, "Invalid Date"), "Not valid")  # Trying to enter invalid score
    #     self.assertEqual(enter_score("Test_User", 1000, "01/01/2005"), "Entered successfully")  # Valid score and date


    # -----------------------------------------------------------------------------

# class TestMethods(unittest.TestCase):
#     # -----------------------------------------------------------------------------
#     # TESTING DB SEARCH
#     def test_valid_search(self):  # Correct username and password
#         self.assertFalse(search("test_user1", "testpassword01", "Users"))
#
#     def test_false_search(self):
#         self.assertFalse(search("test_user1", "incorrectpass", "Users")) # Wrong password
#         self.assertFalse(search("incorrectuser", "testpassword01", "Users"))  # Wrong username
#         self.assertFalse(search("incorrectuser", "incorrectpass", "Users"))  # Both wrong
#
#     def test_invalid_search(self):
#         self.assertFalse(search("", "", "Users"))
#         self.assertFalse(search("test_user1", "", "Users"))
#         self.assertFalse(search("", "testpassword01", "Users"))
    # -----------------------------------------------------------------------------

class TestMethods(unittest.TestCase):
    # -----------------------------------------------------------------------------
    # TESTING VALIDATION

    # testing dates dd/mm/yyyy format
    def test_dates(self):
        self.assertTrue(is_valid_date("01/01/2001"))  # Valid date
        self.assertFalse(is_valid_date("32/13/2001"))  # Invalid date
        self.assertFalse(is_valid_date(2))  # Invalid date, wrong type
        self.assertTrue(is_valid_date("30/12/9999"))  # Extreme (but valid)

    # testing usernames
    def test_users(self):
        self.assertTrue(is_valid_user("test_user1", "username"))  # Valid username
        self.assertFalse(is_valid_user("username_exceeding_chr_limit", "username"))  # Invalid username - too long
        self.assertFalse(is_valid_user(10, "username"))  # Invalid username - wrong type

    # testing passwords
    def test_passwords(self):
        self.assertTrue(is_valid_user("test_password1", "password"))  # Valid password
        self.assertFalse(is_valid_user("test", "password"))  # Invalid password - too short
        self.assertFalse(is_valid_user(True, "password"))  # Invalid password - wrong type
        self.assertTrue(is_valid_user("test1234", "password"))  # Borderline valid

if __name__ == '__main__':
    unittest.main()