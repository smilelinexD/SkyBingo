import tkinter as tk

from pages import *

from pages.main_page import *
from pages.feature_select import *
from pages.bingo_card import *
from pages.goal_detailed import *
import pages.collection_tracker as collection_tracker
import pages.minion_craft_helper as minion_craft_helper
import utils.info_loader as loader
import utils.inventory_utils as inventory_utils


class SkyBingo(tk.Tk):

    def __init__(self):
        super().__init__()
        self.LOADER = loader.Interface()
        self.INVENTORY = inventory_utils.Interface(self.LOADER)
        self.COLLECTION_TRACKER = collection_tracker.Interface(self.LOADER)
        self.MINION_CRAFT_HELPER = minion_craft_helper.Interface(
            self.LOADER, self.INVENTORY)
        self.stack = []
        self.initUI()

    def initUI(self):
        self.title('SkyBingo')
        self.resizable(False, False)

        self.loadBingoGoal()
        self.mainPage = MainPage(self)
        self.stack.append(
            {'name': 'mainPage', 'instance': self.mainPage, 'args': None})
        self.mainPage.pack()

    def showPage(self, name, args=None):
        self.destroyCurrentPage(False)

        if name == 'mainPage':
            instance = self.createMainPage(args)
        elif name == 'featureSelect':
            instance = self.createFeatureSelect(args)
        elif name == 'bingoCard':
            instance = self.createBingoCard(args)
        elif name == 'goalDetailed':
            instance = self.createGoalDetailed(args)
        elif name == 'collectionTrackerMain':
            instance = self.createCollectionTrackerMain(args)
        elif name == 'collectionTrackerType':
            instance = self.createCollectionTrackerType(args)
        elif name == 'collectionTrackerItem':
            instance = self.createCollectionTrackerItem(args)
        elif name == 'minionCraftHelperMain':
            instance = self.createMinionCraftHelperMain(args)
        elif name == 'minionCraftHelperType':
            instance = self.createMinionCraftHelperType(args)
        elif name == 'minionCraftHelperAmountSelect':
            instance = self.createMinionCraftHelperAmountSelect(args)
        elif name == 'minionCraftHelperTrack':
            instance = self.createMinionCraftHelperTrack(args)

        if self.stack[-1]['name'] == name:
            self.stack[-1]['instance'] = instance
        else:
            self.stack.append(
                {'name': name, 'instance': instance, 'args': args})

        self.stack[-1]['instance'].pack()

    def destroyCurrentPage(self, remove):
        page = self.stack[-1]['instance']
        if remove:
            self.stack.pop()
        page.destroy()

    def back(self):
        self.destroyCurrentPage(True)
        self.showPage(self.stack[-1]['name'], self.stack[-1]['args'])

    def createMainPage(self, args):
        self.mainPage = MainPage(self)
        return self.mainPage

    def createFeatureSelect(self, args):
        self.featureSelect = FeatureSelect(self)
        return self.featureSelect

    def createBingoCard(self, args):
        self.bingoCard = BingoCard(self)
        return self.bingoCard

    def createGoalDetailed(self, args):
        i = args[0]
        self.goalDetailed = GoalDetailed(self, i)
        return self.goalDetailed

    def createCollectionTrackerMain(self, args):
        self.collectionTrackerMain = self.COLLECTION_TRACKER.getCollectionTrackerMain(
            self)
        return self.collectionTrackerMain

    def createCollectionTrackerType(self, args):
        type = args[0]
        self.collectionTrackerType = self.COLLECTION_TRACKER.getCollectionTrackerType(
            self, type)
        return self.collectionTrackerType

    def createCollectionTrackerItem(self, args):
        item, numRequired = args
        self.collectionTrackerItem = self.COLLECTION_TRACKER.getCollectionTrackerItem(
            self, item, numRequired=numRequired)
        return self.collectionTrackerItem

    def createMinionCraftHelperMain(self, args):
        self.minionCraftHelperMain = self.MINION_CRAFT_HELPER.getMinionCraftHelperMain(
            self)
        return self.minionCraftHelperMain

    def createMinionCraftHelperType(self, args):
        type = args[0]
        self.minionCraftHelperType = self.MINION_CRAFT_HELPER.getMinionCraftHelperType(
            self, type)
        return self.minionCraftHelperType

    def createMinionCraftHelperAmountSelect(self, args):
        minion = args[0]
        self.minionCraftHelperAmountSelect = self.MINION_CRAFT_HELPER.getMinionCraftHelperAmountSelect(
            self, minion)
        return self.minionCraftHelperAmountSelect

    def createMinionCraftHelperTrack(self, args):
        minion, tier, amount = args
        self.minionCraftHelperTrack = self.MINION_CRAFT_HELPER.getMinionCraftHelperTrack(
            self, minion, tier, amount)
        return self.minionCraftHelperTrack

    def loadBingoGoal(self):
        self.goals = self.LOADER.get_bingo_info()

    def exit(self):
        self.destroy()


if __name__ == '__main__':
    app = SkyBingo()
    app.mainloop()
