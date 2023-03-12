import unittest

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

class TestMethods(unittest.TestCase):
    # -----------------------------------------------------------------------------
    # TESTING VALIDATION
    def test_is_inrange(self):
        data_list = ["test", "1"]
        for data in data_list:
            self.assertTrue(is_inrange(data, 1, 10))
        self.assertFalse(is_inrange("test", 10, 20))
        self.assertEqual(is_inrange(1, 1, 5), "Error")

    def test_is_length(self):
        length_list = [4,1,10]
        for opt in range(1,4):
            self.assertTrue(is_length("test", length_list[opt-1], opt))

        length_list = [5, 5, 1]
        for opt in range(1,4):
            self.assertFalse(is_length("test", length_list[opt-1], opt))

        self.assertIsNot(is_length(1, 2, 1), True)
        self.assertIsNot(is_length(1, 2, 1), False)


