import json

with open('./resources/public/bingo_hint.json', 'r') as f:
    info = json.load(f)

for i, hint in enumerate(info):
    if i > 52:
        break
    # print(hint[11:])
    info[hint]['collectionType'] = hint[11:].upper()
    info[hint]['trackable'] = True
    info[hint]['handler'] = 'collection'

with open('./resources/public/bingo_hint.json', 'w') as f:
    json.dump(info, f)
