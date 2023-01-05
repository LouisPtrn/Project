# ============================================================================================================== #
# File for managing dates
# Written by: Louis Pattern     12/08/2022
# Known bugs:  none
# ============================================================================================================== #

from datetime import *


def get_date():
    return datetime.today().strftime("%d/%m/%Y")


if __name__ == "__main__":
    print(get_date())
