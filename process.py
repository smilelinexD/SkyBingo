import json
from pprint import pprint

with open('./collections.json', 'r') as f:
    info = json.load(f)

for type in info['collections']:
    for item in info['collections'][type]['items']:
        item_name = info['collections'][type]['items'][item]['name']
        with open('./src/{:s}/{:s}.txt'.format(type, item_name), 'w') as f:
            f.write(json.dumps(info['collections'][type]['items'][item]))
        print(item_name)
