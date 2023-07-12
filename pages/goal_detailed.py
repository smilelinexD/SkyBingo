import tkinter as tk
import utils.goal_handler as handler


class GoalDetailed(tk.Frame):
    def __init__(self, master, i):
        super().__init__(master)
        self.master = master
        self.master.geometry('900x520')
        self.i = i
        self.goal = master.goals[i]
        self.HANDLER = handler.Interface()
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

        if 'trackable' in self.goal and self.goal['trackable']:
            btn = tk.Button(self, text='Start Tracking',
                            command=self.track, font=('Arial', 10), width=10)
            btn.grid(row=5, column=1)

    def track(self):
        name, args = self.HANDLER.getHandler(self.goal['handler'], self.goal)
        self.master.showPage(name, args)

    def back(self):
        self.master.back()
