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
    con.close()


def search(u, p):
    con = sqlite3.connect("login.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Users")
    records = cursor.fetchall()
    found = False
    for row in records:
        if row[0] == u and row[1] == p:
            found = True
    return found
    cursor.close()
    con.close()


if __name__ == "__main__":
    createtable()
    print(search("Abid69", "4321"))
