import json
import base64
import nbt
import io

import utils.info_loader as info_loader


class Interface():
    def __init__(self):
        self.LOADER = info_loader.Interface()

        self.collection_variation = None

    def decode_inventory_data(self, raw):
        return nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(raw)))

    def update_inventory_data(self):
        self.inventory_raw = self.LOADER.get_profile_info()[
            'inv_contents']['data']
        inv = self.decode_inventory_data(self.inventory_raw)[0]
        self.inventory = [item for item in inv if len(item) > 0]

    def count_normal_item(self, item_id):
        self.update_inventory_data()

        count = 0
        for item in self.inventory:
            if item['tag']['ExtraAttributes']['id'].value == item_id:
                count += item['Count'].value

        return count

    def count_collection_item(self, item_id, variation):
        if self.collection_variation is None:
            self.collection_variation = self.LOADER.get_collection_variation()

        self.update_inventory_data()

        count = 0
        for item in self.inventory:
            id = item['tag']['ExtraAttributes']['id'].value
            if id in self.collection_variation:
                item_data = self.collection_variation[id]
                if item_data['id'] == item_id and item_data['variation'] == variation:
                    count += item['Count'].value

        return count
