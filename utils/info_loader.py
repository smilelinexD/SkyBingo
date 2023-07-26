import os
import re
import json
import utils.api_contact as api


class Interface():

    def __init__(self):
        self.API = api.Interface()

        self.personal_info = None
        self.bingo_hint = None
        self.bingo_info = None
        self.collection_info_type_menu = None
        self.collection_info_type = None
        self.collection_info_item = None
        self.collection_variation = None
        self.minion_info_type_menu = None
        self.minion_info_type = None
        self.minion_info = None
        self.int_roman_transform = None
        self.item_id_name_transform = None

    def load_personal_info(self):
        file_path = './resources/private/personal_info.json'
        with open(file_path, 'r') as f:
            self.personal_info = json.load(f)

    def load_bingo_hint(self):
        file_path = './resources/public/bingo/bingo_hint.json'
        with open(file_path, 'r') as f:
            self.bingo_hint = json.load(f)

    def load_bingo_info(self):
        if self.bingo_hint is None:
            self.load_bingo_hint()
        self.API.updateBingoInfo()
        file_path = './resources/public/bingo/bingo_info.json'
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

    def load_collection_info_type_menu(self):
        filepath = './resources/public/collection/collection_info_type_menu.json'
        with open(filepath, 'r') as f:
            self.collection_info_type_menu = json.load(f)

    def load_collection_info_type(self):
        filepath = './resources/public/collection/collection_info_type.json'
        with open(filepath, 'r') as f:
            self.collection_info_type = json.load(f)

    def load_collection_info_item(self):
        filepath = './resources/public/collection/collection_info_item.json'
        with open(filepath, 'r') as f:
            self.collection_info_item = json.load(f)

    def load_collection_variation(self):
        filepath = './resources/public/collection/collection_variation.json'
        with open(filepath, 'r') as f:
            self.collection_variation = json.load(f)

    def load_minion_info_type_menu(self):
        filepath = './resources/public/minion/minion_info_type_menu.json'
        with open(filepath, 'r') as f:
            self.minion_info_type_menu = json.load(f)

    def load_minion_info_type(self):
        filepath = './resources/public/minion/minion_info_type.json'
        with open(filepath, 'r') as f:
            self.minion_info_type = json.load(f)

    def load_minion_info(self):
        filepath = './resources/public/minion/minion_info.json'
        with open(filepath, 'r') as f:
            self.minion_info = json.load(f)

    def load_int_roman_transform(self):
        filepath = './resources/public/other/int_roman_transform.json'
        with open(filepath, 'r') as f:
            self.int_roman_transform = json.load(f)

    def load_item_id_name_transform(self):
        filepath = './resources/public/item/item_id_name_transform.json'
        with open(filepath, 'r') as f:
            self.item_id_name_transform = json.load(f)

    def get_personal_info(self):
        if self.personal_info is None:
            self.load_personal_info()
        return self.personal_info

    def get_bingo_hint(self):
        if self.bingo_hint is None:
            self.load_bingo_hint()
        return self.bingo_hint

    def get_bingo_info(self):
        if self.bingo_info is None:
            self.load_bingo_info()
        return self.bingo_info

    def get_profile_info(self):
        return self.API.getProfileInfo()

    def get_collection_info_type_menu(self):
        if self.collection_info_type_menu is None:
            self.load_collection_info_type_menu()
        return self.collection_info_type_menu['Type']

    def get_collection_info_type(self, type_id):
        if self.collection_info_type is None:
            self.load_collection_info_type()
        return self.collection_info_type[type_id]

    def get_collection_info_item(self, item_id):
        if self.collection_info_item is None:
            self.load_collection_info_item()
        return self.collection_info_item[item_id]

    def get_collection_variation(self, item_id):
        if self.collection_variation is None:
            self.load_collection_variation()

        return self.collection_variation[item_id]

    def get_collection_variation_whole(self):
        if self.collection_variation is None:
            self.load_collection_variation()
        return self.collection_variation

    def get_item_value(self, item_id):
        if self.collection_variation is None:
            self.load_collection_variation()
        if item_id not in self.collection_variation:
            return 1
        return self.collection_variation[item_id]['value']

    def get_minion_info_type_menu(self):
        if self.minion_info_type_menu is None:
            self.load_minion_info_type_menu()
        return self.minion_info_type_menu['Type']

    def get_minion_info_type(self, type_id):
        if self.minion_info_type is None:
            self.load_minion_info_type()
        return self.minion_info_type[type_id]

    def get_minion_info(self, minion_id):
        if self.minion_info is None:
            self.load_minion_info()
        return self.minion_info[minion_id]

    def get_int_roman_transform(self):
        if self.int_roman_transform is None:
            self.load_int_roman_transform()
        return self.int_roman_transform

    def get_item_id_name_transform(self):
        if self.item_id_name_transform is None:
            self.load_item_id_name_transform()
        return self.item_id_name_transform


if __name__ == '__main__':
    print(Interface().bingo_info)
