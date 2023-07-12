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
                self.master.showPage('goalDetailed', [i])

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
        self.master.back()
