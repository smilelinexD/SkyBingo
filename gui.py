import tkinter as tk


class SkyBingo(tk.Tk):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.title('SkyBingo')
        self.geometry('800x600')
        self.resizable(False, False)
        self.mainpage = MainPage(self)
        self.mainpage.pack()

    def showMainPage(self):
        self.bingocard.destroy()
        self.mainpage = MainPage(self)
        self.mainpage.pack()

    def showBingoCard(self):
        self.mainpage.destroy()
        self.bingocard = BingoCard(self)
        self.bingocard.pack()

    def loadBingoGoal(self, goals):
        self.goals = goals

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
            goal = goals[i]
            btn = tk.Button(self, text=goal['name'],
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


if __name__ == '__main__':
    app = SkyBingo()
    app.mainloop()
