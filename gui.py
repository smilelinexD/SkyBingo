import tkinter as tk
from PIL import Image, ImageTk
import goal_handler as handler
import utils.info_loader as loader


class SkyBingo(tk.Tk):

    def __init__(self):
        super().__init__()
        self.HANDLER = handler.Worker()
        self.LOADER = loader.Worker()
        self.initUI()

    def initUI(self):
        self.title('SkyBingo')
        self.geometry('800x600')
        self.resizable(False, False)
        self.bingocard = None
        self.goalDetailed = None
        self.goalTrack = None
        self.loadBingoGoal()
        self.showMainPage()

    def showMainPage(self):
        if self.bingocard:
            self.bingocard.destroy()
        self.mainpage = MainPage(self)
        self.mainpage.pack()

    def showBingoCard(self):
        self.mainpage.destroy()
        if self.goalDetailed:
            self.goalDetailed.destroy()
        self.bingocard = BingoCard(self)
        self.bingocard.pack()

    def showGoalDetailed(self, i):
        self.bingocard.destroy()
        if self.goalTrack:
            self.goalTrack.destroy()
        self.goalDetailed = goalDetailed(self, i)
        self.goalDetailed.pack()

    def showGoalTrack(self, i):
        self.goalDetailed.destroy()
        self.goalTrack = goalTrack(self, i)
        self.goalTrack.pack()

    def loadBingoGoal(self):
        self.goals = self.LOADER.bingo_info

    def exit(self):
        self.destroy()


class MainPage(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
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
        self.master.showBingoCard()

    def exit(self):
        self.master.exit()


class BingoCard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.initUI(master.goals)

    def initUI(self, goals):
        btn = tk.Button(self, text='Back', command=self.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)

        for i in range(25):
            def onClick(i=i):
                self.master.showGoalDetailed(i)

            goal = goals[i]
            btn = tk.Button(self, text=goal['name'], command=onClick,
                            font=('Arial', 10), width=15, height=5)

            def onHover(e, i=i):
                self.setDesciption(i)

            btn.bind('<Enter>', onHover)

            if goal['group'] == 'community' or goal['completed']:
                btn.config(bg='green', fg='black')
            else:
                btn.config(bg='red', fg='white')
            btn.grid(row=i // 5 + 1, column=i % 5 + 1)

        self.description = tk.Label(
            self, text='Goal Description', font=('Arial', 10))
        self.description.grid(row=6, column=0, columnspan=6)

    def setDesciption(self, i):
        self.description.config(
            text=self.master.goals[i]['description'])

    def back(self):
        self.master.showMainPage()


class goalDetailed(tk.Frame):
    def __init__(self, master, i):
        super().__init__(master)
        self.master = master
        self.i = i
        self.goal = master.goals[i]
        self.initUI()

    def initUI(self):
        btn = tk.Button(self, text='Back', command=self.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)
        label = tk.Label(self, text=self.goal['name'],
                         font=('Arial', 15), width=25, height=5)
        label.grid(row=1, column=1)
        label = tk.Label(self, text=self.goal['description'],
                         font=('Arial', 15), width=50, height=5)
        label.grid(row=2, column=1, rowspan=2)
        label = tk.Label(self, text=self.goal['hint'],
                         font=('Arial', 10), width=80, height=5)
        label.grid(row=4, column=1)

        def track():
            self.master.showGoalTrack(self.i)

        if 'trackable' in self.goal and self.goal['trackable']:
            btn = tk.Button(self, text='Start Tracking',
                            command=track, font=('Arial', 10), width=10)
            btn.grid(row=5, column=1)

    def back(self):
        self.master.showBingoCard()


class goalTrack(tk.Frame):
    def __init__(self, master, i):
        super().__init__(master)
        self.master = master
        self.i = i
        self.goal = master.goals[i]
        self.goal_info = master.LOADER.get_collection_info(
            self.goal['collectionType'])
        self.handler = master.HANDLER.getHandler(self.goal)
        self.flag = False
        self.INTERVAL = 5
        self.initUI()

    def initUI(self):
        btn = tk.Button(self, text='Back', command=self.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)

        img_name = self.goal_info['img']
        self.img = ImageTk.PhotoImage(Image.open(
            f'./imgs/collection_item/{img_name}').resize((150, 150), Image.ANTIALIAS))
        canvas = tk.Canvas(self, width=200, height=200)
        canvas.create_image(30, 30, anchor='nw', image=self.img)
        canvas.grid(row=1, column=1)

        self.status = tk.Label(self, text=self.goal['name'],
                               font=('Arial', 15), width=25, height=5)
        self.status.grid(row=1, column=2)
        self.flag = True
        self.startTracking()

    def startTracking(self):
        if self.flag:
            self.goal = self.handler.track()
            currentAmount = self.goal['currentAmount']
            requiredAmount = self.goal['requiredAmount']
            status_text = f'{currentAmount}/{requiredAmount} ({currentAmount/requiredAmount*100:.2f}%)'
            self.status.config(text=status_text)
            self.after(self.INTERVAL * 1000, self.startTracking)

    def back(self):
        self.flag = False
        self.master.showGoalDetailed(self.i)


if __name__ == '__main__':
    app = SkyBingo()
    app.mainloop()
