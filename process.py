import json
import ijson

# with open('./resources/public/bingo_hint.json', 'r') as f:
#     info = json.load(f)

# for i, hint in enumerate(info):
#     if i > 52:
#         break
#     # print(hint[11:])
#     # del info[hint]['collectionType']
#     info[hint]['handler'] = ['collectionTrackerItem', hint[11:].upper()]

# with open('./resources/public/bingo_hint.json', 'w') as f:
#     json.dump(info, f)

with open('./resources/public/collection_variation.json', 'r') as f:
    info = json.load(f)

with open('./resources/public/items.json', 'r', encoding='utf-8') as f:
    items = list(ijson.items(f, 'items.item'))

while True:
    try:
        print('Enter collection id: ')
        id = input()
        if id == '-1':
            break
        while True:
            print('Enter variation id: ')
            variation = int(input())
            if variation == -1:
                break
            while True:
                print('Enter item name: ')
                item = input()
                if item == '-1':
                    break
                print('Enter value: ')
                value = int(input())

                flag = True

                for i in items:
                    if i['name'] == item:
                        flag = False
                        info[i['id']] = {"id": id, "value": value,
                                         "variation": variation, "name": item}
                        break

                if flag:
                    print('=====Item not found=====')
                else:
                    with open('./resources/public/collection_variation.json', 'w') as f:
                        json.dump(info, f)
                    print('=====Item added=====')

    except KeyboardInterrupt:
        break
