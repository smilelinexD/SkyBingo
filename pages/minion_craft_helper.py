import tkinter as tk
from PIL import Image, ImageTk
from idlelib.tooltip import Hovertip
from functools import partial


class Interface():
    def __init__(self, loader):
        self.LOADER = loader

    def getMinionCraftHelperMain(self, master):
        master.geometry('650x250')
        return MinionCraftHelperMain(master, self.LOADER)

    def getMinionCraftHelperType(self, master, type):
        master.geometry('650x250')
        return MinionCraftHelperType(master, type, self.LOADER)


class MinionCraftHelperMain(tk.Frame):
    def __init__(self, master, loader):
        super().__init__(master)
        self.master = master
        self.LOADER = loader

        self.minion_types = self.LOADER.get_minion_info_type_menu()
        self.img_list = list()
        self.initUI()

    def initUI(self):
        btn = tk.Button(self, text='Back', command=self.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)

        for i, type in enumerate(self.minion_types):
            type_info = self.LOADER.get_minion_info_type(type)
            img_path = type_info['img']
            self.img_list.append(ImageTk.PhotoImage(Image.open(
                f'./imgs/{img_path}').resize((100, 100), Image.ANTIALIAS)))
            btn = tk.Button(self, image=self.img_list[i], command=partial(
                self.showMinionCraftHelperType, type))
            Hovertip(btn, type_info['name'], hover_delay=300)
            btn.grid(row=1, column=i + 1)

    def showMinionCraftHelperType(self, type):
        self.master.showPage('minionCraftHelperType', [type])

    def back(self):
        self.master.back()


class MinionCraftHelperType(tk.Frame):
    def __init__(self, master, type, loader):
        super().__init__(master)
        self.master = master
        self.LOADER = loader
        self.type = type
        self.minions = self.LOADER.get_minion_info_type(type)[
            'list']
        self.img_list = list()
        self.initUI()

    def initUI(self):
        btn = tk.Button(self, text='Back', command=self.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)

        for i, minion in enumerate(self.minions):
            minion_info = self.LOADER.get_minion_info(minion)
            img_path = minion_info['img']
            self.img_list.append(ImageTk.PhotoImage(Image.open(
                f'./imgs/{img_path}icon.webp').resize((64, 100), Image.ANTIALIAS)))
            btn = tk.Button(self, image=self.img_list[i], command=partial(
                self.showMinionCraftHelperItem, minion))
            Hovertip(btn, minion_info['name'], hover_delay=300)
            btn.grid(row=int(i / 7 + 1), column=i % 7 + 1)

    def showMinionCraftHelperItem(self, item):
        self.master.showPage('minionCraftHelperItem', [item, None])

    def back(self):
        self.master.back()
