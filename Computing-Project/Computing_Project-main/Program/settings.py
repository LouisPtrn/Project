# ============================================================================================================== #
# This file is used for writing and reading to the settings text file
# Written by: Louis Pattern     08/08/2022
# Known bugs: none
# ============================================================================================================== #


def get_setting(st):
    # Returns the value for a given setting
    try:
        st = st.upper()
        lines = []
        item = ""
        # Dictionary for each line of the text file representing a setting
        st_dict = {"WIDTH": 0, "HEIGHT": 1, "DIFFICULTY": 2, "COLOUR": 3}

        with open("saved_settings.TXT") as f:
            for line in f:
                lines.append(line.strip())

        target = lines[st_dict[st]]
        i = target.find(":") + 2
        while i < len(target):
            item += target[i]
            i += 1
        return item
    except KeyError:
        return "Setting not found"


def save_setting(st, data):
    st = st.upper()
    lines = []
    st_dict = {"WIDTH": 0, "HEIGHT": 1, "DIFFICULTY": 2, "COLOUR": 3}

    with open("saved_settings.TXT") as f:
        for line in f:
            lines.append(line.strip())

    target = lines[st_dict[st]]
    i = target.find(":") + 2
    n = 0
    new_item = ""
    while n < i:
        new_item += target[n]
        n += 1
    new_item += data
    lines[st_dict[st]] = new_item

    with open("saved_settings.TXT", "w") as f:
        for items in lines:
            f.write(items + "\n")


def load_defualts():
    # Resets text file to default settings
    open("saved_settings.TXT", "w").close()
    with open("saved_settings.TXT", "a") as f:
        f.write("Window width: " + "960" + "\n")
        f.write("Window height: " + "540" + "\n")
        f.write("Difficulty: " + "Normal" + "\n")
        f.write("Colourblind mode: " + "False")


# Creates the text file after first launch
def remember_launch():
    with open("I_remember_you.TXT", "w") as f:
        f.write("")


# Checks if the text file exits
def is_first_launch():
    try:
        with open("I_remember_you.TXT"):
            pass
        return False
    except FileNotFoundError:
        return True


if __name__ == "__main__":
    print(get_setting("colour"))
    save_setting("colour", "True")