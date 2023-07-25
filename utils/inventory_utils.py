import json
import base64
import nbt
import io


class Interface():
    def __init__(self, loader):
        self.LOADER = loader

        self.collection_variation = None

    def decode_inventory_data(self, raw):
        return nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(raw)))

    def update_inventory_data(self):
        self.inventory_raw = self.LOADER.get_profile_info()[
            'inv_contents']['data']
        inv = self.decode_inventory_data(self.inventory_raw)[0]
        self.inventory = [item for item in inv if len(item) > 0]

    def count_normal_item(self, item_id, update=True):
        if update:
            self.update_inventory_data()

        count = 0
        for item in self.inventory:
            if item['tag']['ExtraAttributes']['id'].value == item_id:
                count += item['Count'].value

        return count

    def count_collection_item(self, item_id, variation, update=True):
        if update:
            self.update_inventory_data()
        if self.collection_variation is None:
            self.collection_variation = self.LOADER.get_collection_variation()

        count = 0
        for item in self.inventory:
            id = item['tag']['ExtraAttributes']['id'].value
            if id in self.collection_variation:
                item_data = self.collection_variation[id]
                if item_data['id'] == item_id and item_data['variation'] == variation:
                    count += item['Count'].value * item_data['value']

        return count

    def count_minion(self, minion_id, update=True):
        if update:
            self.update_inventory_data()

        inventory_minion = {i: 0 for i in range(1, 12)}
        done = 0
        for item in self.inventory:
            id = item['tag']['ExtraAttributes']['id'].value
            if id.startswith(minion_id):
                tier = int(id.split('_')[-1])
                inventory_minion[tier] += 1

        return inventory_minion
