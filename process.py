import json
import ijson
import utils.info_loader as info_loader

LOADER = info_loader.Interface()

item_id_name_transform = LOADER.get_item_id_name_transform()
id_to_name = item_id_name_transform['id_to_name']
name_to_id = item_id_name_transform['name_to_id']

filepath = './resources/public/minion/minion_info.json'

with open(filepath, 'r') as f:
    info = json.load(f)
while True:
    print('Collection Type:')
    collection_type = input()
    if collection_type == '':
        break
    while True:
        data = dict()
        print('Minion Name: (without \'minion\')')
        minion_name = input()
        if minion_name == '':
            break
        minion_id = name_to_id[f'{minion_name} Minion I'][:-2]
        data['name'] = f'{minion_name} Minion'
        img = '_'.join(minion_id.split('_')[:-1]).lower()
        data['img'] = f'minion/{collection_type}/{img}'
        # collection_name = minion_name
        while True:
            print('Collection Name:')
            collection_name = input()
            if collection_name == '':
                collection_name = minion_name
            if collection_name in name_to_id:
                break
        data['collection_id'] = name_to_id[collection_name]

        print('Max Tier:')
        max_tier = int(input())

        recipe = dict()
        until = -1
        for i in range(1, max_tier + 1):
            print(f'Tier {i}')
            print('itemA Name:')
            if i > until:
                while True:
                    itemA_name = input().replace('E ', 'Enchanted ')
                    if itemA_name in name_to_id:
                        break
                    print('itemA Name:')
                itemA_id = name_to_id[itemA_name]
                print('until?')
                until = int(input())
            else:
                print(itemA_name)
            print('itemA amount:')
            itemA_amount = int(input())
            if i == 1:
                while True:
                    print('itemB Name: (without \'Wooden\')')
                    itemB_name = 'Wooden ' + input()
                    if itemB_name in name_to_id:
                        break
                # itemB_name = input()
                itemB_id = name_to_id[itemB_name]
            else:
                itemB_id = f'{minion_id}_{i - 1}'
                # itemB_name = id_to_name[itemB_id]

            item_variation = LOADER.get_collection_variation(itemA_id)

            item_list = list()
            item_list.append(
                {'item_id': itemA_id, 'required': itemA_amount})
            item_list.append(
                {'item_id': itemB_id, 'required': 1})

            recipe[i] = item_list

        data['recipe'] = recipe

        info[minion_id] = data

        with open(filepath, 'w') as f:
            json.dump(info, f)
