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
        self.top = self.winfo_toplevel()
        self.top.rowconfigure(0,weight=1)
        self.top.columnconfigure(0, weight=1)

        self.power_on = tk.Button(self)
        self.power_on.grid(row=1, column=0, columnspan=1, sticky=('N', 'S', 'E', 'W'))
        self.power_on["command"] = lambda: print('power_on')
        self.power_on["text"] = "Power ON"

        self.power_off = tk.Button(self)
        self.power_off.grid(row=1, column=1, columnspan=1, sticky=('N', 'S', 'E', 'W'))
        self.power_off["command"] = lambda: print('power off')
        self.power_off["text"] = "Power OFF"

        self.createMenuBar()


    def createMenuBar(self):
        self.menu_bar = tk.Menu(root)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Set serial port", command=lambda: print('set serial port'))
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit', command=root.quit)

        self.status_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.status_menu.add_command(label="Get general status", command=lambda: print('get gen stat'))
        self.status_menu.add_command(label="Get lamp hours", command=lambda: print('get lamp hours'))
        self.status_menu.add_command(label="Get input", command=lambda: print('get input'))


        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Status", menu=self.status_menu)

        root.config(menu=self.menu_bar)



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
