import tkinter as tk

from pages import *

from pages.main_page import *
from pages.feature_select import *
from pages.bingo_card import *
from pages.goal_detailed import *
import pages.collection_tracker as collection_tracker
import utils.info_loader as loader


class SkyBingo(tk.Tk):

    def __init__(self):
        super().__init__()
        self.LOADER = loader.Interface()
        self.stack = []
        self.initUI()

    def initUI(self):
        self.title('SkyBingo')
        self.resizable(False, False)

        self.COLLECTION_TRACKER = collection_tracker.Interface(self.LOADER)

        self.loadBingoGoal()
        self.mainPage = MainPage(self)
        self.stack.append(
            {'name': 'mainPage', 'instance': self.mainPage, 'args': None})
        self.mainPage.pack()

    def showPage(self, name, args):
        self.destroyCurrentPage(False)

        if name == 'mainPage':
            self.createMainPage()
        elif name == 'featureSelect':
            self.createFeatureSelect()
        elif name == 'bingoCard':
            self.createBingoCard()
        elif name == 'goalDetailed':
            self.createGoalDetailed(args[0])
        elif name == 'collectionTrackerMain':
            self.createCollectionTrackerMain()
        elif name == 'collectionTrackerType':
            self.createCollectionTrackerType(args[0])
        elif name == 'collectionTrackerItem':
            self.createCollectionTrackerItem(args[0], args[1])

        self.stack[-1]['instance'].pack()

    def destroyCurrentPage(self, remove):
        page = self.stack[-1]['instance']
        if remove:
            self.stack.pop()
        page.destroy()

    def back(self):
        self.destroyCurrentPage(True)
        self.showPage(self.stack[-1]['name'], self.stack[-1]['args'])

    def createMainPage(self):
        self.mainPage = MainPage(self)
        if self.stack[-1]['name'] == 'mainPage':
            self.stack[-1]['instance'] = self.mainPage
        else:
            self.stack.append(
                {'name': 'mainPage', 'instance': self.mainPage, 'args': None})

    def createFeatureSelect(self):
        self.featureSelect = FeatureSelect(self)
        if self.stack[-1]['name'] == 'featureSelect':
            self.stack[-1]['instance'] = self.featureSelect
        else:
            self.stack.append(
                {'name': 'featureSelect', 'instance': self.featureSelect, 'args': None})

    def createBingoCard(self):
        self.bingoCard = BingoCard(self)
        if self.stack[-1]['name'] == 'bingoCard':
            self.stack[-1]['instance'] = self.bingoCard
        else:
            self.stack.append(
                {'name': 'bingoCard', 'instance': self.bingoCard, 'args': None})

    def createGoalDetailed(self, i):
        self.goalDetailed = GoalDetailed(self, i)
        if self.stack[-1]['name'] == 'goalDetailed':
            self.stack[-1]['instance'] = self.goalDetailed
        else:
            self.stack.append(
                {'name': 'goalDetailed', 'instance': self.goalDetailed, 'args': [i]})

    def createCollectionTrackerMain(self):
        self.collectionTrackerMain = self.COLLECTION_TRACKER.getCollectionTrackerMain(
            self)
        if self.stack[-1]['name'] == 'collectionTrackerMain':
            self.stack[-1]['instance'] = self.collectionTrackerMain
        else:
            self.stack.append({'name': 'collectionTackerMain',
                               'instance': self.collectionTrackerMain, 'args': None})

    def createCollectionTrackerType(self, type):
        self.collectionTrackerType = collection_tracker.Interface(self.LOADER
                                                                  ).getCollectionTrackType(type, self)
        if self.stack[-1]['name'] == 'collectionTrackerType':
            self.stack[-1]['instance'] = self.collectionTrackerType
        else:
            self.stack.append({'name': 'collectionTrackerType',
                               'instance': self.collectionTrackerType, 'args': [type]})

    def createCollectionTrackerItem(self, item, numRequired):
        self.collectionTrackerItem = collection_tracker.CollectionTrackerItem(
            self, item, self.LOADER, numRequired=numRequired)
        if self.stack[-1]['name'] == 'collectionTrackerItem':
            self.stack[-1]['instance'] = self.collectionTrackerItem
        else:
            self.stack.append({'name': 'collectionTrackerItem',
                               'instance': self.collectionTrackerItem, 'args': [item, numRequired]})

    def loadBingoGoal(self):
        self.goals = self.LOADER.bingo_info

    def exit(self):
        self.destroy()


if __name__ == '__main__':
    app = SkyBingo()
    app.mainloop()
