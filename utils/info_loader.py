import os
import json
import utils.api_contact as api


class Worker():

    def __init__(self):
        self.API = api.Worker()

        self.load_personal_info()
        self.load_bingo_hint()
        self.load_bingo_info()

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
                goal['group'], goal['name'], goal['hint'] = hint['group'], hint['name'], hint['hint']
                goal['description'] = hint['description'].format(
                    goal['requiredAmount']) if hint['hasRequiredAmount'] else hint['description']
            else:
                name = goal['name']
                print(f'goal {name} has no hint.')


if __name__ == '__main__':
    print(Worker().bingo_info)
