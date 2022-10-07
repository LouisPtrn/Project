# ============================================================================================================== #
# This file will be used for validation only.
# Written by: Louis Pattern     09/05/2022
# Known bugs: none
# ============================================================================================================== #

from datetime import *


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
    except Exception as ex:
        return ex


# range validation
def is_inrange(data, lo, hi):
    try:
        if (len(data) >= lo) and (len(data) <= hi):
            return True
        return False
    except ValueError:
        return "Error 2"


# username and password validation
# u - data to be validated, opt - validation option: username or password
def is_valid_user(u, opt):
    if opt == "username":
        if isinstance(u, str):
            if len(u) > 3 and len(u) <= 20:
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
        if isinstance(u, str) and len(u) > 7:
            valid = True
    return valid


# Checks is a given date is valid
def is_valid_date(given_date):  # DD/MM/YYYY
    try:
        datetime.strptime(given_date, '%d/%m/%Y')
        return True
    except ValueError:
        return False


# Checks if a high score is valid - positive integer that isn't too high
def is_valid_score(score):
    if isinstance(score, int):
        if 0 <= score < 1000000:
            return True
    return False


if __name__ == "__main__":
    # show_message("Test1", (is_length(True, 15, 3)), 2)
    # if is_inrange("test", 1, 2):
    #     show_message("Range", "Value is in range", 1)
    # else:
    # if not is_valid_date("29/02/2005"):
    #     show_message("Date", "Date is invalide", 3)
    pass