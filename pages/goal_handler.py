import re
import time
import tkinter as tk
from PIL import Image, ImageTk
import utils.info_loader as loader


class Worker():
    def __init__(self):
        self.info = loader.Interface()

    def getHandler(self, master, goal):
        handler = goal['handler']
        if handler == 'collection':
            return collectionHandler(master, goal, self.info)


class collectionHandler():
    def __init__(self, master, goal, loader):
        self.master = master
        self.goal = goal
        self.loader = loader
        self.flag = True

        self.goal_info = self.loader.get_collection_info(
            self.goal['collectionType'])

        self.initUI()

    def initUI(self):
        btn = tk.Button(self.master, text='Back', command=self.master.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)

        img_name = self.goal_info['img']
        self.img = ImageTk.PhotoImage(Image.open(
            f'./imgs/collection_item/{img_name}').resize((150, 150), Image.ANTIALIAS))
        canvas = tk.Canvas(self.master, width=200, height=200)
        canvas.create_image(30, 30, anchor='nw', image=self.img)
        canvas.grid(row=1, column=1)

        self.status = tk.Label(self.master, text=self.goal['name'],
                               font=('Arial', 15), width=25, height=5)
        self.status.grid(row=1, column=2)

    def track(self):
        print('track')
        profile = self.loader.get_profile_info()
        collection = profile['collection']
        if self.goal['collectionType'] not in collection:
            self.goal['currentAmount'] = 0
        else:
            self.goal['currentAmount'] = collection[self.goal['collectionType']]

        currentAmount = self.goal['currentAmount']
        requiredAmount = self.goal['requiredAmount']
        status_text = f'{currentAmount}/{requiredAmount} ({currentAmount/requiredAmount*100:.2f}%)'
        self.status.configure(text=status_text)

    def trackLoop(self):
        while self.flag:
            try:
                self.track()
                time.sleep(self.master.INTERVAL)
            except KeyboardInterrupt:
                self.flag = False

    def stop(self):
        self.flag = False


class collectionLevel7Handler():
    def __init__(self, master, goal, loader):
        self.master = master
        self.goal = goal
        self.loader = loader
        self.flag = True

        self.goal_info = self.loader.get_collection_info(
            self.goal['collectionType'])

        self.initUI()

    def initUI(self):
        btn = tk.Button(self.master, text='Back', command=self.master.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)

        img_name = self.goal_info['img']
        self.img = ImageTk.PhotoImage(Image.open(
            f'./imgs/collection_item/{img_name}').resize((150, 150), Image.ANTIALIAS))
        canvas = tk.Canvas(self.master, width=200, height=200)
        canvas.create_image(30, 30, anchor='nw', image=self.img)
        canvas.grid(row=1, column=1)

        self.status = tk.Label(self.master, text=self.goal['name'],
                               font=('Arial', 15), width=25, height=5)
        self.status.grid(row=1, column=2)

    def track(self):
        print('track')
        profile = self.loader.get_profile_info()
        collection = profile['collection']
        if self.goal['collectionType'] not in collection:
            self.goal['currentAmount'] = 0
        else:
            self.goal['currentAmount'] = collection[self.goal['collectionType']]

        currentAmount = self.goal['currentAmount']
        requiredAmount = self.goal['requiredAmount']
        status_text = f'{currentAmount}/{requiredAmount} ({currentAmount/requiredAmount*100:.2f}%)'
        self.status.configure(text=status_text)

    def trackLoop(self):
        while self.flag:
            try:
                self.track()
                time.sleep(self.master.INTERVAL)
            except KeyboardInterrupt:
                self.flag = False

    def stop(self):
        self.flag = False


if __name__ == '__main__':
    goal = {
        "id": "collection_sand",
        "name": "Sand Collector",
        "lore": "Reach 60,000 Sand Collection.",
        "description": "Reach 60,000 Sand Collection.",
        "requiredAmount": 60000,
        "completed": True,
        "group": "collection",
        "hint": "NO",
        "collectionType": "SAND",
    }
    worker = Worker()
    handler = worker.getHandler(goal)
    handler.trackLoop()
