

class Interface():
    def __init__(self):
        pass

    def getHandler(self, handler, goal):
        if handler[0] == 'collectionTrackerItem':
            handler.append(goal['requiredAmount'])
            return handler[0], handler[1:]
