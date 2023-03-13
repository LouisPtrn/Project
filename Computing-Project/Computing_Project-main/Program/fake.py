import unittest
from validation import *

def is_inrange(data, lo, hi):
    try:
        if (len(data) >= lo) and (len(data) <= hi):
            return True
        return False
    except TypeError:
        return "Error"

def is_length(data, length, opt):
    try:
        if opt == 1:
            if len(data) == length:
                return True
            return False
        elif opt == 2:
            if len(data) >= length:
                return True
            return False
        elif opt == 3:
            if len(data) <= length:
                return True
            return False
    except Exception as ex:
        return ex

def is_valid_user(u, opt):
    if opt == "username":
        if isinstance(u, str):
            if is_inrange(u, 3, 20):
                u = u.upper()
                characters = []
                for i in range(65, 91):
                    characters.append(chr(i))
                for i in range(48, 58):
                    characters.append(chr(i))
                characters.append("_")
                valid = True
                for n in range(len(u)):
                    if not u[n] in characters:
                        valid = False
            else:
                valid = False
        else:
            valid = False
    else:
        valid = False
        if isinstance(u, str) and is_inrange(u, 8, 255):
            valid = True
    return valid


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

if __name__ == "__main__":
    unittest.main()