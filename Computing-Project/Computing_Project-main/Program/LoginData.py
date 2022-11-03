# ============================================================================================================== #
# File for managing the login database
# Written by: Louis Pattern     08/08/2022
# ============================================================================================================== #

import sqlite3
import validation
import bcrypt
from messages import *


def create_table():
    con = sqlite3.connect("LoginScores.db")
    con.execute('''CREATE TABLE IF NOT EXISTS Users
                (Username VARCHAR PRIMARY KEY NOT NULL,
                Password TEXT                NOT NULL);''')

    con.execute('''CREATE TABLE IF NOT EXISTS Admins
                    (Username VARCHAR PRIMARY KEY NOT NULL,
                    Password TEXT                NOT NULL);''')
    # add initial data
    hashable_pw = bytes("IHaveNoHandsAndIMustCode", encoding='utf-8')
    con.execute('''insert into Admins  (Username, Password) values (?, ?)''',
                ("AdminLouis_0001", bcrypt.hashpw(hashable_pw, bcrypt.gensalt())))
    con.commit()
    con.close()


def enter_user(u, p):
    # Validation performed on username and password before they are entered
    val_u = validation.is_valid_user(u, "username")
    val_p = validation.is_valid_user(p, "password")
    if val_u and val_p:
        con = sqlite3.connect("LoginScores.db")
        p = bytes(p, encoding='utf-8')
        hash_p = bcrypt.hashpw(p, bcrypt.gensalt())
        try:
            con.execute('''insert into Users (Username, Password) values (?, ?)''',
                        (u, hash_p))
            con.commit()
            con.close()
            return True
        except Exception as ex:
            show_message("Error creating user", ex, 2)
            con.close()
            return False
    else:
        return False


def search(u, p, table):
    con = sqlite3.connect("LoginScores.db")
    cursor = con.cursor()
    p = bytes(p, encoding='utf-8')

    if table == "Admins":
        cursor.execute("SELECT * FROM Admins")
    else:
        cursor.execute("SELECT * FROM Users")
    records = cursor.fetchall()
    found = False
    for row in records:
        if row[0] == u and bcrypt.checkpw(p, row[1]):
            found = True
    cursor.close()
    con.close()
    return found


def is_existent_user(u):
    con = sqlite3.connect("LoginScores.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Users")
    records = cursor.fetchall()
    found = False
    for row in records:
        if row[0] == u:
            found = True
    cursor.close()
    con.close()
    return found


def delete_user(u):
    if is_existent_user(u):
        try:
            con = sqlite3.connect("LoginScores.db")
            cursor = con.cursor()
            # Deleting single record now
            sql = "DELETE FROM Users WHERE Username=?"
            cursor.execute(sql, (u,))
            con.commit()
            cursor.close()
            con.close()
            show_message("Success", "User deleted ", 1)

        except sqlite3.Error as error:
            # Displays popup message rather than printing
            show_message("Error", "Failed to delete record from sqlite table: " + str(error), 2)
    else:
        show_message("Error", "User does not exist", 3)


if __name__ == "__main__":
    create_table()
    print(search("Dave_112233", "123456789", "Users"))
