import json
import ijson

with open('./resources/public/collection/collection_info.json', 'r') as f:
    info = json.load(f)

for i, c in enumerate(info):
    if i <= 6:
        continue
    del info[c]['hasMinion']


with open('./resources/public/collection/collection_info.json', 'w') as f:
    json.dump(info, f)
