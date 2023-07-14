import tkinter as tk
from PIL import Image, ImageTk
from idlelib.tooltip import Hovertip
from functools import partial


class Interface():
    def __init__(self, loader):
        self.LOADER = loader

    def getMinionCraftHelperMain(self, master):
        master.geometry('650x250')
        return MinionCraftHelperMain(master)

    # def getCollectionTrackType(self, type, master):
    #     master.geometry('650x250')
    #     return CollectionTrackerType(type, master, self.LOADER)


class MinionCraftHelperMain(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.initUI()

    def initUI(self):
        btn = tk.Button(self, text='Back', command=self.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)

        label = tk.Label(self, text='Minion Craft Helper')
        label.grid(row=1, column=1)

    def back(self):
        self.master.back()
