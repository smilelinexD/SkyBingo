import tkinter as tk
from PIL import Image, ImageTk
from idlelib.tooltip import Hovertip
from functools import partial


class Interface():
    def __init__(self, loader):
        self.loader = loader

    def getCollectionTrackerMain(self, master):
        master.geometry('650x250')
        return CollectionTrackerMain(master, self.loader)

    def getCollectionTrackType(self, type, master):
        master.geometry('650x250')
        return CollectionTrackerType(type, master, self.loader)


class CollectionTrackerMain(tk.Frame):
    def __init__(self, master, loader):
        super().__init__(master)
        self.master = master
        self.loader = loader

        self.collection_types = loader.get_collection_info_main()
        self.img_list = list()
        self.initUI()

    def initUI(self):
        btn = tk.Button(self, text='Back', command=self.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)

        for i, type in enumerate(self.collection_types):
            type_info = self.loader.get_collection_info_type(type)
            img_path = type_info['img']
            self.img_list.append(ImageTk.PhotoImage(Image.open(
                f'./imgs/collection_item/{img_path}').resize((100, 100), Image.ANTIALIAS)))
            btn = tk.Button(self, image=self.img_list[i], command=partial(
                self.showCollectionType, type))
            Hovertip(btn, type.capitalize() + ' Collections', hover_delay=300)
            if i <= 4:
                btn.grid(row=1, column=i + 1)
            else:
                btn.grid(row=2, column=i - 2)

    def showCollectionType(self, type):
        self.master.showCollectionTrackerType(type)

    def back(self):
        self.master.showFeatureSelect()


class CollectionTrackerType(tk.Frame):
    def __init__(self, type, master, loader):
        super().__init__(master)
        self.master = master
        self.loader = loader
        self.type = type
        self.collection_items = loader.get_collection_info_type(type)['list']
        self.img_list = list()
        self.initUI()

    def initUI(self):
        btn = tk.Button(self, text='Back', command=self.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)

        for i, item in enumerate(self.collection_items):
            item_info = self.loader.get_collection_info_item(item)
            img_path = item_info['img']
            self.img_list.append(ImageTk.PhotoImage(Image.open(
                f'./imgs/collection_item/{img_path}').resize((64, 64), Image.ANTIALIAS)))
            btn = tk.Button(self, image=self.img_list[i], command=partial(
                self.showCollectionTrackerItem, item))
            Hovertip(btn, item.capitalize(), hover_delay=300)
            btn.grid(row=int(i / 7 + 1), column=i % 7 + 1)

    def showCollectionTrackerItem(self, item):
        self.master.showCollectionTrackerItem(
            item, 'collectionTracker', self.type)

    def back(self):
        self.master.showCollectionTrackerMain()


class CollectionTrackerItem(tk.Frame):
    def __init__(self, master, item, caller, id, loader):
        super().__init__(master)
        self.master = master
        self.master.geometry('500x250')
        self.item = item
        self.caller = caller
        self.id = id
        self.loader = loader
        self.collection_info = self.loader.get_collection_info_item(self.item)
        self.INTTOROMAN = self.loader.get_int_to_roman()
        self.flag = True
        self.INTERVAL = 5
        self.initUI()

    def initUI(self):
        btn = tk.Button(self, text='Back', command=partial(
            self.back, self.caller, self.id))
        btn.grid(row=0, column=0)

        self.item_img = ImageTk.PhotoImage(
            Image.open('./imgs/collection_item/' + self.collection_info['img']).resize((180, 180), Image.ANTIALIAS))
        label = tk.Label(self, image=self.item_img)
        label.grid(row=1, column=1)
        self.track_text = tk.Label(self, text=self.item, font=('Arial', 20))
        self.track_text.grid(row=1, column=2)

    def track(self):
        if self.flag:
            # print('track')
            profile = self.loader.get_profile_info()
            if self.item in profile['collection']:
                self.item_count = profile['collection'][self.item]
            else:
                self.item_count = 0

            if self.caller == 'collectionTracker':
                i = 0
                requirements = self.collection_info['levelRequirements']
                print(self.item_count, requirements)
                while i < len(requirements) and self.item_count >= requirements[i]:
                    i += 1
                print(i)
                if i == len(requirements):
                    text = f'{self.INTTOROMAN[str(i)]} MAX'
                else:
                    text = f'{self.INTTOROMAN[str(i)]} {self.item_count}/{requirements[i]}'
                self.track_text.configure(text=text)
            self.after(self.INTERVAL * 1000, self.track)

    def back(self, to, id):
        self.flag = False
        if to == 'collectionTracker':
            self.master.showCollectionTrackerType(id)
