# ============================================================================================================== #
# Admin window file
# Written by: Louis Pattern     23/08/2022
# Known bugs:
# ============================================================================================================== #

from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox
from messages import *
import LoginData
import login


class AdminWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.menubar = Menu(self)
        self.title("Admin Window")
        self.config(bg='#CDE2FF')
        self.geometry("600x360")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')
        # title
        self.label = ttk.Label(self, text='Welcome admin', font=("Helvetica", 25, "bold"))
        self.label.pack()

        # text entry boxes
        self.entry1 = tk.Entry(self, bd=6, width=40)
        self.entry1.place(x=250, y=100)
        self.entry2 = tk.Entry(self, bd=6, width=40)
        self.entry2.place(x=250, y=150)
        self.entry2.config(show="*")
        self.entry3 = tk.Entry(self, bd=6, width=40)
        self.entry3.place(x=250, y=180)
        self.entry3.config(show="*")
        self.i = True

        # create user button
        self.button = ttk.Button(self, text='Create User')
        self.button['command'] = lambda: self.create_user()
        self.button.place(x=475, y=300)
        self.bind("<Return>", (lambda event: self.create_user()))

        # delete user button
        self.button = ttk.Button(self, text='Delete User')
        self.button['command'] = lambda: self.delete_user()
        self.button.place(x=50, y=300)

        # exit dropdown menu
        self.config(menu=self.menubar)
        file_menu = Menu(self.menubar)
        file_menu.add_command(label='User Menu', command=self.go_back)
        file_menu.add_command(label='Quit', command=self.destroy)
        self.menubar.add_cascade(label="File", menu=file_menu, underline=0)

        # username and password text
        self.label = ttk.Label(self, text='New User Name:', font=("Arial", 15))
        self.label.place(x=75, y=100)
        self.label = ttk.Label(self, text='Password:', font=("Arial", 15))
        self.label.place(x=75, y=150)
        self.label = ttk.Label(self, text='Re-enter password', font=("Arial", 15))
        self.label.place(x=75, y=180)

        # show password checkbox
        self.check1 = tk.Checkbutton(self, text='Show Password', onvalue=True, offvalue=False)
        self.check1['command'] = lambda: self.togglepass()
        self.check1.place(x=420, y=220)

    def togglepass(self):
        if self.i:
            self.entry2.config(show="")
            self.i = False
        else:
            self.entry2.config(show="*")
            self.i = True

    def create_user(self):
        username = self.entry1.get()
        password = self.entry2.get()
        confirm = self.entry3.get()
        # Checks the passwords match before attempting to create user
        if password == confirm:
            if LoginData.enter_user(username, password):
                show_message("Success", "Entered user", 1)
            else:
                show_message("Error", "Invalid user", 3)
        else:
            show_message("Error", "Passwords do not match", 3)

    def delete_user(self):
        username = self.entry1.get()
        LoginData.delete_user(username)

    def go_back(self):
        AdminWindow.destroy(self)
        login.create_window()

    def cancel(self):
        ans = tk.messagebox.askyesno(title='', message='Exit?')
        if ans:
            AdminWindow.destroy(self)
            login.create_window()


def create_window():
    admin_login = AdminWindow()
    admin_login.mainloop()


if __name__ == "__main__":
    create_window()
