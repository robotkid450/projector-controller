#!/usr/bin/env python3

import SanyoProtocol
import tkinter as tk
from tkinter import messagebox

__version__ = '1.0'

class projectorControlInterface(tk.Frame):
    """docstring for projectorControlInterface."""
    def __init__(self, master=None, projector=None):
        tk.Frame.__init__(self, master)
        self.projector = projector
