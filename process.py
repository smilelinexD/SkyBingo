import json

with open('./resources/public/bingo_hint.json', 'r') as f:
    info = json.load(f)

for i, hint in enumerate(info):
    if i > 52:
        break
    # print(hint[11:])
    # del info[hint]['collectionType']
    info[hint]['handler'] = ['collectionTrackerItem', hint[11:].upper()]

with open('./resources/public/bingo_hint.json', 'w') as f:
    json.dump(info, f)
