import tkinter as tk
from tkinter import Menu

root = tk.Tk()
root.title = ("Menu test")
menubar = Menu(root)
root.config(menu=menubar)
file_menu = Menu(menubar)
file_menu.add_command(label='Exit', command=root.destroy,)
file_menu.add_command(label='Exit2', command=root.destroy,)
file_menu.add_command(label='Exit3', command=root.destroy,)
file_menu.add_command(label='Exit4', command=root.destroy,)
menubar.add_cascade(label="File", menu=file_menu, underline=0)

root.mainloop()