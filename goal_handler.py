import re
import time
import utils.info_loader as loader


class Worker():
    def __init__(self):
        self.info = loader.Worker()
        self.INTERVAL = 5

    def getHandler(self, goal):
        handler = goal['handler']
        if handler == 'collection':
            return collectionHandler(self, goal)


class collectionHandler():
    def __init__(self, master, goal):
        self.master = master
        self.goal = goal
        self.flag = True

    def track(self):
        profile = self.master.info.load_profile_info()
        collection = profile['collection']
        if self.goal['collectionType'] not in collection:
            self.goal['currentAmount'] = 0
        else:
            self.goal['currentAmount'] = collection[self.goal['collectionType']]

        return self.goal

    def trackLoop(self):
        while self.flag:
            try:
                self.track()
                time.sleep(self.master.INTERVAL)
            except KeyboardInterrupt:
                self.flag = False

    def stop(self):
        self.flag = False


if __name__ == '__main__':
    goal = {
        "id": "collection_sand",
        "name": "Sand Collector",
        "lore": "Reach 60,000 Sand Collection.",
        "description": "Reach 60,000 Sand Collection.",
        "requiredAmount": 60000,
        "completed": True,
        "group": "collection",
        "hint": "NO",
        "collectionType": "SAND",
    }
    worker = Worker()
    handler = worker.getHandler(goal)
    handler.trackLoop()
