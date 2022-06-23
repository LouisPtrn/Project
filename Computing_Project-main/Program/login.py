# ============================================================================================================== #
# This file will be used for logging in only.
# Written by: Louis Pattern     11/05/2022
# Known bugs: none
# ============================================================================================================== #

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from logindata import search


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login Window")
        self.geometry("600x350")
        self.iconbitmap("H:/Computing-Project/Program/graphics/yinyang.ico")  # Window icon  C:/Users/patte/Computing Project/Program/graphics/yinyang.ico
        # title
        self.label = ttk.Label(self, text='Welcome, Please Log In.', font=("Helvetica",25,"bold"))
        self.label.pack()

        # login button
        self.button = ttk.Button(self, text='Login')
        self.button['command'] = lambda: self.login(self.entry1, self.entry2)
        self.button.place(x=475, y=300)

        # cancel button
        self.button = ttk.Button(self, text='Cancel', width=10)
        self.button['command'] = self.cancel
        self.button.place(x=50, y=300)

        # username and password text
        self.label = ttk.Label(self, text='User Name:', font=("Arial", 15))
        self.label.place(x=75, y=100)
        self.label = ttk.Label(self, text='Password:', font=("Arial", 15))
        self.label.place(x=75, y=150)

        # text entry boxes
        self.entry1 = tk.Entry(self, bd=6, width=40)
        self.entry1.place(x=250, y=100)
        self.entry2 = tk.Entry(self, bd=6, width=40)
        self.entry2.place(x=250, y=150)

    def login(self, username, password):
        username = username.get()
        password = password.get()
        found = search(str(username), str(password))
        if found:
            tk.messagebox.showinfo(title='', message="Welcome "+username)
        else:
            tk.messagebox.showinfo(title='', message="No")

    def cancel(self):
        ans = tk.messagebox.askyesno(title='', message='Exit?')
        if ans:
            LoginWindow.destroy(self)


if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()