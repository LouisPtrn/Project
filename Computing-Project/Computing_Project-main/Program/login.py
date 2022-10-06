# ============================================================================================================== #
# This file will be used for logging in only.
# Written by: Louis Pattern     24/06/2022
# Known bugs: 0 When exiting game, quit button can be clicked multiple times causes many messages (FIXED)
# ============================================================================================================== #

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from LoginData import search
import game
import AdminControl


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login Window")
        self.geometry("600x350")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')
        # Window icon
        self.iconbitmap("graphics/saturn.ico")
        # title
        self.label = ttk.Label(self, text='Welcome, Please Log In.', font=("Helvetica", 25, "bold"))
        self.label.pack()

        # text entry boxes
        self.entry1 = tk.Entry(self, bd=6, width=40)
        self.entry1.place(x=250, y=100)
        self.entry2 = tk.Entry(self, bd=6, width=40)
        self.entry2.place(x=250, y=150)
        self.entry2.config(show="*")
        self.i = True

        # login button
        self.button = ttk.Button(self, text='Login')
        self.button['command'] = lambda: self.log_in()
        self.button.place(x=475, y=300)
        self.bind("<Return>", (lambda event: self.log_in()))

        # exit button
        self.button2 = ttk.Button(self, text='Quit', width=10)
        self.button2['command'] = self.cancel
        self.button2.place(x=50, y=300)
        self.bind("<Escape>", (lambda event: self.cancel()))

        # username and password text
        self.label = ttk.Label(self, text='User Name:', font=("Arial", 15))
        self.label.place(x=75, y=100)
        self.label = ttk.Label(self, text='Password:', font=("Arial", 15))
        self.label.place(x=75, y=150)

        # show password checkbox
        self.check1 = tk.Checkbutton(self, text='Show Password', onvalue=True, offvalue=False)
        self.check1['command'] = lambda: self.toggle_pass()
        self.check1.place(x=420, y=220)

    def toggle_pass(self):
        # Show or hide password box
        if self.i:
            self.entry2.config(show="")
            self.i = False
        else:
            self.entry2.config(show="*")
            self.i = True

    def log_in(self):
        username = self.entry1.get()
        password = self.entry2.get()
        if search(str(username), str(password), "Users"):
            tk.messagebox.showinfo(title='', message="Welcome " + username)
            LoginWindow.destroy(self)
            game.setup()
            game.play(username)
        elif search(str(username), str(password), "Admins"):
            tk.messagebox.showinfo(title='', message="Welcome admin " + username)
            LoginWindow.destroy(self)
            AdminControl.create_window()
        else:
            tk.messagebox.showinfo(title='', message="No")

    def cancel(self):
        ans = tk.messagebox.askyesno(title='', message='Exit?')
        if ans:
            LoginWindow.destroy(self)
            quit()


def create_window():
    login = LoginWindow()
    login.mainloop()


def restart(username):
    game.setup()
    game.play(username)


if __name__ == "__main__":
    create_window()
