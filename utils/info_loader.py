import os
import re
import json
import utils.api_contact as api


class Worker():

    def __init__(self):
        self.API = api.Worker()

        self.load_personal_info()
        self.load_bingo_hint()
        self.load_bingo_info()
        self.load_collection_info()

    def load_personal_info(self):
        file_path = './resources/private/personal_info.json'
        with open(file_path, 'r') as f:
            self.personal_info = json.load(f)

    def load_bingo_hint(self):
        file_path = './resources/public/bingo_hint.json'
        with open(file_path, 'r') as f:
            self.bingo_hint = json.load(f)

    def load_bingo_info(self):
        file_path = './resources/public/bingo_info.json'
        with open(file_path, 'r') as f:
            self.bingo_info = json.load(f)['goals']
        for goal in self.bingo_info:
            if goal['id'] in self.bingo_hint:
                hint = self.bingo_hint[goal['id']]
                goal['group'], goal['hint'] = hint['group'], hint['hint']
                if 'lore' in goal:
                    goal['description'] = re.sub('\u00a7.', '', goal['lore'])
                else:
                    # Community goals
                    goal['description'] = hint['description']
                goal['trackable'] = hint['trackable'] if 'trackable' in hint else False
                goal['collectionType'] = hint['collectionType'] if 'collectionType' in hint else None
                goal['handler'] = hint['handler'] if 'handler' in hint else None
                goal['raw_hint'] = hint
            else:
                name = goal['name']
                print(f'goal {name} has no hint.')

    def load_profile_info(self):
        return self.API.getProfileInfo()

    def load_collection_info(self):
        filepath = './resources/public/collection_info.json'
        with open(filepath, 'r') as f:
            self.collection_info = json.load(f)

    def get_collection_info(self, collection_id):
        return self.collection_info[collection_id]


if __name__ == '__main__':
    print(Worker().bingo_info)
