import utils.info_loader as loader
import gui


if __name__ == '__main__':
    info = loader.Worker()
    app = gui.SkyBingo()
    app.loadBingoGoal(info.bingo_info)
    app.mainloop()
    pass
