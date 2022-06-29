# ============================================================================================================== #
# This file will be used for outputting messages only.
# Written by: Louis Pattern     16/05/2022
# Known bugs: none
# ============================================================================================================== #

from tkinter import messagebox


# Options: 1-show info, 2-show error, 3-show warning, 4-ask y/n
def show_message(title, message, opt):
    if opt == 1:
        messagebox.showinfo(title=title, message=message)
    elif opt == 2:
        messagebox.showerror(title=title, message=message)
    elif opt == 3:
        messagebox.showwarning(title=title, message=message)
    elif opt == 4:
        messagebox.askyesno(title=title, message=message)


if __name__ == "__main__":
    show_message("Test", "Abid?", 4)
