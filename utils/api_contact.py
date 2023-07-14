import requests
import json
import os
from datetime import date


class Interface():
    def __init__(self):
        self.TIMESTAMP = date.today().strftime('%Y-%m')
        self.loadAPIKey()
        self.checkPersonalInfoAvailable()
        self.UUID = self.personal_info['uuid']
        self.checkBingoInfoAvailable()

    def loadAPIKey(self):
        with open('./resources/private/API_KEY.json', 'r') as f:
            file = json.load(f)
            self.API_KEY = file['Key']

    def checkPersonalInfoAvailable(self):
        print('Checking personal info availability...')
        if not os.path.isfile('./resources/private/personal_info.json'):
            print('Personal info not found.')
            # TODO Get username from input
            username = 'smilelinexD'
            self.createPersonalInfo(username)
            return
        with open('./resources/private/personal_info.json', 'r') as f:
            info = json.load(f)
            self.username = info['username']
            if info['timestamp'] == self.TIMESTAMP:
                self.personal_info = info
                print('Personal info available!')
                return
            else:
                print('Personal info outdated.')
                self.updatePersonalInfo()
                return

    def createPersonalInfo(self, username):
        print('Creating personal info file...')
        # Request uuid from Mojang API
        url_uuid = f'https://api.mojang.com/users/profiles/minecraft/{username}'
        responce = requests.get(url_uuid).json()
        if 'errorMessage' in responce:
            raise Exception(
                'Couldn\'t find any profile with this username')
        uuid = responce['id']
        personal_info = {'username': username, 'uuid': uuid}
        with open('./resources/private/personal_info.json', 'w') as f:
            json.dump(personal_info, f)
        print('Created basic personal info file!')

        self.updatePersonalInfo()

    def updatePersonalInfo(self):
        print('Updating personal info...')
        # Get basic information from file
        with open('./resources/private/personal_info.json', 'r') as f:
            personal_info = json.load(f)
        username, uuid = personal_info['username'], personal_info['uuid']

        # Request profile list from Hypixel API
        payload_profiles = {'key': self.API_KEY, 'uuid': uuid}
        responce = requests.get(
            'https://api.hypixel.net/skyblock/profiles', params=payload_profiles).json()
        if not responce['success']:
            raise Exception(responce['cause'])
        profile_id = None
        for p in responce['profiles']:
            if 'game_mode' in p and p['game_mode'] == 'bingo':
                profile_id = p['profile_id']
                break
        if profile_id is None:
            raise Exception('This user does nott have a bingo profile!')

        # Record
        self.personal_info = {'username': username, 'uuid': uuid,
                              'profile_id': profile_id, 'timestamp': self.TIMESTAMP}
        with open('./resources/private/personal_info.json', 'w') as f:
            json.dump(self.personal_info, f)
        print('Update done!')

    def checkBingoInfoAvailable(self):
        print('Checking bingo info availability...')
        if not os.path.isfile('./resources/public/bingo/bingo_info.json'):
            print('Bingo info not found.')
            self.createBingoInfo()
            return
        with open('./resources/public/bingo/bingo_info.json', 'r') as f:
            info = json.load(f)
            if info['timestamp'] == self.TIMESTAMP:
                self.bingo_info = info
                print('Bingo info available!')
                return
            else:
                print('Bingo info outdated.')
                self.createBingoInfo()
                return

    def createBingoInfo(self):
        ''' Creating bingo_info file, or update for the first time every month
        '''
        print('Start creating bingo info...')
        payload = {'key': self.API_KEY}
        responce = requests.get(
            'https://api.hypixel.net/resources/skyblock/bingo', params=payload).json()
        if not responce['success']:
            raise Exception(responce['cause'])
        self.bingo_info = responce
        self.bingo_info['timestamp'] = self.TIMESTAMP
        for i, g in enumerate(self.bingo_info['goals']):
            # Add completed attribute to non community goal
            if i % 6 != 0:
                g['completed'] = False
        with open('./bingo_info.json', 'w') as f:
            json.dump(self.bingo_info, f)
        print('Bingo info creation done!')

    def getProfileInfo(self, dumping=False):
        # Request particular profile info from Hypixel API
        payload = {'key': self.API_KEY,
                   'profile': self.personal_info['profile_id']}
        responce = requests.get(
            'https://api.hypixel.net/skyblock/profile', params=payload).json()
        if not responce['success']:
            raise Exception(responce['cause'])
        if dumping:
            with open('./resources/private/profile.json', 'w') as f:
                json.dump(responce, f)
        return responce['profile']['members'][self.UUID]

    def updateBingoInfo(self):
        print('Checking if each goal completed...')
        payload = {'key': self.API_KEY, 'uuid': self.UUID}
        responce = requests.get(
            'https://api.hypixel.net/skyblock/bingo', params=payload).json()
        if not responce['success']:
            raise Exception(responce['cause'])
        completed_goals = responce['events'][-1]['completed_goals']

        for goal in self.bingo_info['goals']:
            if goal['id'] in completed_goals:
                goal['completed'] = True

        with open('./resources/public/bingo/bingo_info.json', 'w') as f:
            json.dump(self.bingo_info, f)
        print('Check done!')


if __name__ == '__main__':
    i = Interface()

    profile_id = 'b7358da7-520b-4e55-958b-5e2a75df8f80'

    payload = {'key': i.API_KEY,
               'profile': profile_id}
    responce = requests.get(
        'https://api.hypixel.net/skyblock/profile', params=payload).json()
    if not responce['success']:
        raise Exception(responce['cause'])
    with open('./tmp.json', 'w') as f:
        json.dump(responce, f)
