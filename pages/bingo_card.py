import tkinter as tk


class BingoCard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.geometry('900x520')
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
        self.master.showFeatureSelect()


class GoalDetailed(tk.Frame):
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

        # def track():
        #     self.master.showGoalTrack(self.i)

        # if 'trackable' in self.goal and self.goal['trackable']:
        #     btn = tk.Button(self, text='Start Tracking',
        #                     command=track, font=('Arial', 10), width=10)
        #     btn.grid(row=5, column=1)

    def back(self):
        self.master.showBingoCard()
