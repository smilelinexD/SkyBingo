import os
import time
import utils.api_contact as api

personal_info = None


def getCollection():
    profile_info = api.getProfileInfo()
    uuid = personal_info['uuid']
    return profile_info['profile']['members'][uuid]['collection']


def showCollection(collection, name, ID):
    print(f'{name}: {collection[ID]}')


def main():
    try:
        while True:
            os.system('cls')
            collection = getCollection()
            showCollection(collection, 'Mithril', 'MITHRIL_ORE')
            # showCollection(collection, 'Sponge', 'SPONGE')
            for _ in tqdm(range(60), bar_format='[{bar}]'):
                time.sleep(1)
    except KeyboardInterrupt:
        key = input('enter R to resume, or anything else to leave:\n')
        return key == 'r' or key == 'R'


if __name__ == '__main__':
    personal_info, bingo_info = api.initialize()
    for g in bingo_info['goals']:
        print(g)
    # print(bingo_info['goals'])
    # while main():
    #     pass
    print('exiting')
