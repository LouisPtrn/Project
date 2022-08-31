# ============================================================================================================== #
# File for managing the login database
# Written by: Louis Pattern     08/08/2022
# ============================================================================================================== #

import sqlite3
import validation
from messages import *


def createtable():
    con = sqlite3.connect("login.db")
    con.execute('''CREATE TABLE IF NOT EXISTS Users
                (Username INT PRIMARY KEY NOT NULL,
                Password TEXT                NOT NULL);''')
    # add test data
    # con.execute('''insert into users  (Username, Password) values (?, ?)''',
    #              ("LouisP", "4321"))
    # con.commit()
    con.execute('''CREATE TABLE IF NOT EXISTS Admins
                    (Username INT PRIMARY KEY NOT NULL,
                    Password TEXT                NOT NULL);''')
    # add test data
    # con.execute('''insert into Admins  (Username, Password) values (?, ?)''',
    #              ("Admin0001", "12345678"))
    # con.commit()
    con.close()


def enter_user(u, p):
    val_u = validation.is_valid_user(u, "username")
    val_p = validation.is_valid_user(p, "password")
    if val_u and val_p:
        con = sqlite3.connect("login.db")
        try:
            con.execute('''insert into Users (Username, Password) values (?, ?)''',
                        (u, p))
            con.commit()
            con.close()
            return True
        except Exception as ex:
            print(ex)
            con.close()
            return False
    else:
        print("not valid")


def search(u, p, table):
    con = sqlite3.connect("login.db")
    cursor = con.cursor()
    if table == "Admins":
        cursor.execute("SELECT * FROM Admins")
    else:
        cursor.execute("SELECT * FROM Users")
    records = cursor.fetchall()
    found = False
    for row in records:
        if row[0] == u and row[1] == p:
            found = True
    cursor.close()
    con.close()
    return found


def delete_user(u):
    try:
        con = sqlite3.connect("login.db")
        cursor = con.cursor()
        # Deleting single record now
        sql = "DELETE FROM Users WHERE Username=?"
        cursor.execute(sql, (u,))
        con.commit()
        cursor.close()
        con.close()

    except sqlite3.Error as error:
        # Displays popup message rather than printing
        show_message("Error", "Failed to delete record from sqlite table: " + str(error), 1)


if __name__ == "__main__":
    createtable()
    # enter_user("Richard_11", "Password1")
    # delete_user("Richard_11")
    delete_user(int)
