# ============================================================================================================== #
# File for managing the highscores database
# Written by: Louis Pattern     08/08/2022
# ============================================================================================================== #

import sqlite3
import validation


def createtable():
    con = sqlite3.connect("Highscores.db")
    con.execute('''CREATE TABLE IF NOT EXISTS Highscores
                (ID INT PRIMARY KEY NOT NULL,
                Name INT                 NOT NULL,
                Score INT                NOT NULL,
                Date TEXT                NOT NULL);''')
    # add test data
    # a = gen_id("James", 5000, "03/03/2003")
    # con.execute('''insert into Highscores  (ID, Name, Score, Date) values (?, ?, ?, ?)''',
    #             (a, "James", 5000, "03/03/2003"))
    con.commit()
    con.close()


def enter_score(name, score, date):
    val_d = validation.is_valid_date(date)
    val_s = validation.is_valid_score(score)
    entry_id = gen_id(name, score, date)
    if val_d and val_s:
        con = sqlite3.connect("Highscores.db")
        try:
            con.execute('''insert into Highscores (ID, Name, Score, Date) values (?, ?, ?, ?)''',
                        (entry_id, name, score, date))
            con.commit()
            con.close()
            return "Entered successfully"
        except Exception as ex:
            con.close()
            return ex

    else:
        return "Not valid"


# Returns a list of names in descending score order
def get_names():
    names = []
    con = sqlite3.connect("Highscores.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM Highscores ORDER BY Score DESC")
    records = cursor.fetchall()
    for row in records:
        names.append(row[1])

    cursor.close()
    con.close()
    return names


# Returns the list of scores in descending score order
def get_scores():
    scores = []
    con = sqlite3.connect("Highscores.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM Highscores ORDER BY Score DESC")
    records = cursor.fetchall()
    for row in records:
        scores.append(row[2])

    cursor.close()
    con.close()
    return scores


# Generates a hexidecimal ID for a given, username, score and date
def gen_id(name, score, date):
    en_id = 0
    for i in name:
        en_id = en_id + (ord(i))

    en_id = int(en_id) + score
    date_num = int(date[:2]) * int(date[3:5]) * int(date[6:])

    en_id += date_num
    return hex(en_id)


if __name__ == "__main__":
    # createtable()
    # print(get_scores())
    print(enter_score("Abid", 15000, "01/04/2004"))
