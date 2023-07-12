import tkinter as tk


class MainPage(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.geometry('520x520')
        self.initUI()

    def initUI(self):
        label = tk.Label(self, text='SkyBingo',
                         font=('Arial', 50), width=10, height=5)
        label.grid(row=0, column=0)
        btn = tk.Button(self, text='Start',
                        command=self.start, font=('Arial', 20))
        btn.grid(row=1, column=0)
        btn = tk.Button(self, text='Exit', command=self.exit,
                        font=('Arial', 20))
        btn.grid(row=2, column=0)

    def start(self):
        self.master.showPage('featureSelect', None)

    def exit(self):
        self.master.exit()
