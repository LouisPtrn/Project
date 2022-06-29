# ============================================================================================================== #
# This file will be used for validation only.
# Written by: Louis Pattern     09/05/2022
# Known bugs: none
# ============================================================================================================== #

from messages import *

# length validation
# parameters: data - data that needs to be validated  length(int) - length to compare data to


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
    except:
        return "Error 1"


# range validation
def is_inrange(data, lo, hi):
    try:
        if (len(data) >= lo) and (len(data) <= hi):
            return True
        return False
    except:
        return "Error 2"


if __name__ == "__main__":
    show_message("Test1", (is_length(True, 15, 3)), 2)
    if is_inrange("test", 1, 2):
        show_message("Range", "Value is in range", 1)
    else:
        show_message("Range", "Value is not in range", 3)
