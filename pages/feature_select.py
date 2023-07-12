import tkinter as tk


class FeatureSelect(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.geometry('900x520')
        self.initUI()

    def initUI(self):
        btn = tk.Button(self, text='back', command=self.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)
        btn = tk.Button(self, text='Show Bingo Card',
                        command=self.showBingoCard, font=('Arial', 15), width=15, height=5)
        btn.grid(row=1, column=1)
        btn = tk.Button(self, text='Collection Tracker', command=self.showCollectionTrackerMain,
                        font=('Arial', 15), width=15, height=5)
        btn.grid(row=1, column=2)

    def back(self):
        self.master.back()

    def showBingoCard(self):
        self.master.showPage('bingoCard', None)

    def showCollectionTrackerMain(self):
        self.master.showPage('collectionTrackerMain', None)
