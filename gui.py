import tkinter as tk

from pages import *

from pages.main_page import *
from pages.feature_select import *
from pages.bingo_card import *
import pages.collection_tracker as collection_tracker
import utils.info_loader as loader


class SkyBingo(tk.Tk):

    def __init__(self):
        super().__init__()
        self.LOADER = loader.Interface()
        self.initUI()

    def initUI(self):
        self.title('SkyBingo')
        self.resizable(False, False)
        self.featureSelect = None
        self.bingoCard = None
        self.goalDetailed = None

        self.COLLECTION_TRACKER = collection_tracker.Interface(self.LOADER)
        self.collectionTrackerMain = None
        self.collectionTrackerType = None
        self.collectionTrackerItem = None

        self.goalTrack = None
        self.loadBingoGoal()
        self.showMainPage()

    def showMainPage(self):
        if self.featureSelect:
            self.featureSelect.destroy()
        if self.bingoCard:
            self.bingoCard.destroy()
        self.mainPage = MainPage(self)
        self.mainPage.pack()

    def showFeatureSelect(self):
        self.mainPage.destroy()
        if self.bingoCard:
            self.bingoCard.destroy()
        if self.collectionTrackerMain:
            self.collectionTrackerMain.destroy()
        self.featureSelect = FeatureSelect(self)
        self.featureSelect.pack()

    def showBingoCard(self):
        self.featureSelect.destroy()
        if self.goalDetailed:
            self.goalDetailed.destroy()
        self.bingoCard = BingoCard(self)
        self.bingoCard.pack()

    def showGoalDetailed(self, i):
        self.bingoCard.destroy()
        if self.goalTrack:
            self.goalTrack.destroy()
        self.goalDetailed = GoalDetailed(self, i)
        self.goalDetailed.pack()

    def showCollectionTrackerMain(self):
        self.featureSelect.destroy()
        if self.collectionTrackerType:
            self.collectionTrackerType.destroy()
        self.collectionTrackerMain = self.COLLECTION_TRACKER.getCollectionTrackerMain(
            self)
        self.collectionTrackerMain.pack()

    def showCollectionTrackerType(self, type):
        self.collectionTrackerMain.destroy()
        if self.collectionTrackerItem:
            self.collectionTrackerItem.destroy()
        self.collectionTrackerType = collection_tracker.Interface(self.LOADER
                                                                  ).getCollectionTrackType(type, self)
        self.collectionTrackerType.pack()

    def showCollectionTrackerItem(self, item, caller, id):
        self.collectionTrackerType.destroy()
        self.collectionTrackerItem = collection_tracker.CollectionTrackerItem(
            self, item, caller, id, self.LOADER)
        self.collectionTrackerItem.pack()
        self.collectionTrackerItem.track()

    def loadBingoGoal(self):
        self.goals = self.LOADER.bingo_info

    def exit(self):
        self.destroy()


if __name__ == '__main__':
    app = SkyBingo()
    app.mainloop()
