#!/usr/bin/env python3

import SanyoProtocol
import tkinter as tk
from tkinter import messagebox

__version__ = '1.0'

stickyVal = ('N', 'S', 'E', 'W')

class projectorControlInterface(tk.Frame):
    """docstring for projectorControlInterface."""
    def __init__(self, master=None, projector=None):
        tk.Frame.__init__(self, master)
        self.projector = projector
        self.grid(sticky=stickyVal)

        self.createWidgets()

    def createWidgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0, weight=1)

        self.test_button = tk.Button(self)
        self.test_button.grid(row=0, column=0, columnspan=1, sticky=('N', 'S', 'E', 'W'))

# runs main application
def run():
    global root
    root = tk.Tk()
    root.title("Projector Control")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = projectorControlInterface(master=root)
    app.mainloop()

if __name__ == '__main__':
    run()
