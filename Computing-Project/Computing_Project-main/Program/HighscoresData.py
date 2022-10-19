# ============================================================================================================== #
# File for managing the highscores database
# Written by: Louis Pattern     08/08/2022
# ============================================================================================================== #

import sqlite3
import Dates
import validation


def create_h_table():
    con = sqlite3.connect("LoginScores.db")
    con.execute("PRAGMA foreign_keys = 1")
    con.execute('''CREATE TABLE IF NOT EXISTS Highscores
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name INT(24)                 NOT NULL,
                Score INT                NOT NULL,
                Date TEXT(16)               NOT NULL,
                FOREIGN KEY (Name) REFERENCES Users(Username));''')
    # add default data
    for i in range(5):
        enter_score(" ", 0, Dates.get_date())
    con.commit()
    con.close()


def enter_score(name, score, date):
    val_d = validation.is_valid_date(date)
    val_s = validation.is_valid_score(score)
    if val_d and val_s:
        con = sqlite3.connect("LoginScores.db")
        try:
            con.execute('''insert into Highscores (Name, Score, Date) values (?, ?, ?)''',
                        (name, score, date))
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
    con = sqlite3.connect("LoginScores.db")
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
    con = sqlite3.connect("LoginScores.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM Highscores ORDER BY Score DESC")
    records = cursor.fetchall()
    for row in records:
        scores.append(row[2])

    cursor.close()
    con.close()
    return scores


def reset_scores():
    con = sqlite3.connect("LoginScores.db")
    cursor = con.cursor()
    cursor.execute("DROP TABLE Highscores")
    create_h_table()


if __name__ == "__main__":
    # create_h_table()
    reset_scores()
