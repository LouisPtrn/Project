import sqlite3


def createtable():
    con = sqlite3.connect("login.db")
    con.execute('''CREATE TABLE IF NOT EXISTS Users
                (Username INT PRIMARY KEY NOT NULL,
                Password TEXT                NOT NULL);''')
    # add test data
    # con.execute('''insert into users  (Username, Password) values (?, ?)''',
    #              ("Abid69", "4321"))
    # con.commit()
    con.execute('''CREATE TABLE IF NOT EXISTS Admins
                    (Username INT PRIMARY KEY NOT NULL,
                    Password TEXT                NOT NULL);''')
    # add test data
    # con.execute('''insert into Admins  (Username, Password) values (?, ?)''',
    #              ("Admin0001", "12345678"))
    # con.commit()
    con.close()


def enteruser(u, p):
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


if __name__ == "__main__":
    createtable()
    print(search("Admin0001", "12345678", "Admins"))
    # enteruser("Dave", "1111")
