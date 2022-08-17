# ============================================================================================================== #
# This file is only used for displaying messages and alerts
# Written by: Louis Pattern     08/08/2022
# Known bugs: none
# ============================================================================================================== #

import tkinter as tk
from tkinter import messagebox


# Options: 1-show info, 2-show error, 3-show warning, 4-ask y/n
def show_message(title, message, opt):
    root = tk.Tk()
    root.withdraw()  # Hides tk window immediately
    if opt == 1:
        messagebox.showinfo(title=title, message=message)
    elif opt == 2:
        messagebox.showerror(title=title, message=message)
    elif opt == 3:
        messagebox.showwarning(title=title, message=message)
    elif opt == 4:
        return(messagebox.askyesno(title=title, message=message))
    root.destroy()

if __name__ == "__main__":
    show_message("Test", "Testing?", 4)
