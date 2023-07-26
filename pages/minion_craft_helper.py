import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from idlelib.tooltip import Hovertip
from functools import partial


class Interface():
    def __init__(self, loader, inventory):
        self.LOADER = loader
        self.INVENTORY = inventory

    def getMinionCraftHelperMain(self, master):
        master.geometry('650x250')
        return MinionCraftHelperMain(master, self.LOADER)

    def getMinionCraftHelperType(self, master, type):
        master.geometry('650x250')
        return MinionCraftHelperType(master, type, self.LOADER)

    def getMinionCraftHelperAmountSelect(self, master, minion):
        master.geometry('650x250')
        return MinionCraftHelperAmountSelect(master, minion, self.LOADER)

    def getMinionCraftHelperTrack(self, master, minion, tier, amount):
        master.geometry('650x250')
        return MinionCraftHelperTrack(master, minion, tier, amount, self.LOADER, self.INVENTORY)


class MinionCraftHelperMain(tk.Frame):
    def __init__(self, master, loader):
        super().__init__(master)
        self.master = master
        self.LOADER = loader

        self.minion_types = self.LOADER.get_minion_info_type_menu()
        self.img_list = list()
        self.initUI()

    def initUI(self):
        btn = tk.Button(self, text='Back', command=self.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)

        for i, type in enumerate(self.minion_types):
            type_info = self.LOADER.get_minion_info_type(type)
            img_path = type_info['img']
            self.img_list.append(ImageTk.PhotoImage(Image.open(
                f'./imgs/{img_path}').resize((100, 100), Image.ANTIALIAS)))
            btn = tk.Button(self, image=self.img_list[i], command=partial(
                self.showMinionCraftHelperType, type))
            Hovertip(btn, type_info['name'], hover_delay=300)
            btn.grid(row=1, column=i + 1)

    def showMinionCraftHelperType(self, type):
        self.master.showPage('minionCraftHelperType', [type])

    def back(self):
        self.master.back()


class MinionCraftHelperType(tk.Frame):
    def __init__(self, master, type, loader):
        super().__init__(master)
        self.master = master
        self.LOADER = loader
        self.type = type
        self.minions = self.LOADER.get_minion_info_type(type)[
            'list']
        self.img_list = list()
        self.initUI()

    def initUI(self):
        btn = tk.Button(self, text='Back', command=self.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)

        for i, minion in enumerate(self.minions):
            minion_info = self.LOADER.get_minion_info(minion)
            img_path = minion_info['img']
            self.img_list.append(ImageTk.PhotoImage(Image.open(
                f'./imgs/{img_path}/icon.webp').resize((64, 100), Image.ANTIALIAS)))
            btn = tk.Button(self, image=self.img_list[i], command=partial(
                self.showMinionCraftHelperAmountSelect, minion))
            Hovertip(btn, minion_info['name'], hover_delay=300)
            btn.grid(row=int(i / 7 + 1), column=i % 7 + 1)

    def showMinionCraftHelperAmountSelect(self, minion):
        self.master.showPage('minionCraftHelperAmountSelect', [minion])

    def back(self):
        self.master.back()


class MinionCraftHelperAmountSelect(tk.Frame):
    def __init__(self, master, minion, loader):
        super().__init__(master)
        self.master = master
        self.LOADER = loader
        self.minion = minion
        self.minion_info = self.LOADER.get_minion_info(minion)
        self.minion_name = self.minion_info['name']
        int_roman_transform = self.LOADER.get_int_roman_transform()
        self.INT_TO_ROMAN = int_roman_transform['int_to_roman']
        self.ROMAN_TO_INT = int_roman_transform['roman_to_int']
        self.img_list = list()

        self.tier = 1
        self.amount = 1

        self.initUI()

    def initUI(self):
        btn = tk.Button(self, text='Back', command=self.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)

        tier_roman = self.INT_TO_ROMAN[str(self.tier)]
        self.label_name = tk.Label(
            self, text=f'{self.minion_name} {tier_roman}', font=('Arial', 20))
        self.label_name.grid(row=1, column=1)

        for i in range(1, 12):
            self.img_list.append(ImageTk.PhotoImage(Image.open(
                f'./imgs/{self.minion_info["img"]}/{i}.webp').resize((64, 64), Image.ANTIALIAS)))

        self.label_img = tk.Label(self, image=self.img_list[0])
        self.label_img.grid(row=2, column=1)

        label = tk.Label(self, text='Tier', font=('Arial', 20))
        label.grid(row=1, column=2)

        combox_val = [self.INT_TO_ROMAN[str(i)] for i in range(1, 12)]
        self.combox_tier = ttk.Combobox(
            self, values=combox_val, state='readonly')
        self.combox_tier.current(0)
        self.combox_tier.bind('<<ComboboxSelected>>', self.updateTier)
        self.combox_tier.grid(row=2, column=2)

        label = tk.Label(self, text='Amount', font=('Arial', 20))
        label.grid(row=1, column=3)

        self.entry_var = tk.IntVar(value=1)
        self.entry_amount = tk.Entry(
            self, textvariable=self.entry_var, width=10)
        # self.entry_amount.insert(0, '1')
        self.entry_amount.grid(row=2, column=3)
        self.entry_var.trace_add('write', self.updateAmount)

        btn = tk.Button(self, text='Track',
                        command=self.showMinionCraftHelperTrack, font=('Arial', 20))
        btn.grid(row=3, column=2)

    def updateTier(self, evt):
        self.tier = self.ROMAN_TO_INT[self.combox_tier.get()]

        tier_roman = self.INT_TO_ROMAN[str(self.tier)]
        self.label_name.configure(text=f'{self.minion_name} {tier_roman}')

        self.label_img.configure(image=self.img_list[self.tier - 1])

    def updateAmount(self, *args):
        if self.entry_amount.get() == '':
            self.entry_var.set(1)
        self.amount = self.entry_var.get()

    def showMinionCraftHelperTrack(self):
        if self.amount <= 0:
            return
        self.master.showPage('minionCraftHelperTrack', [
                             self.minion, self.tier, self.amount])

    def back(self):
        self.master.back()


class MinionCraftHelperTrack(tk.Frame):
    def __init__(self, master, minion, tier, amount, loader, inventory):
        super().__init__(master)
        self.master = master
        self.LOADER = loader

        item_id_name_transform = self.LOADER.get_item_id_name_transform()
        self.ID_TO_NAME = item_id_name_transform['id_to_name']
        self.NAME_TO_ID = item_id_name_transform['name_to_id']
        self.INT_TO_ROMAN = self.LOADER.get_int_roman_transform()[
            'int_to_roman']

        self.minion = minion
        self.minion_info = self.LOADER.get_minion_info(minion)
        self.collection_id = self.minion_info['collection_id']
        self.collection_name = self.ID_TO_NAME[self.collection_id]
        self.recipe = self.minion_info['recipe'][str(tier)]
        self.item_list = self.recipe['item_list']
        self.minion_name = self.minion_info['name']
        self.tier = tier
        self.amount = amount
        self.INVENTORY = inventory
        self.img_dict_minion = dict()
        self.img_dict_item = dict()
        self.textVar_list = list()
        self.flag = True
        self.can_craft = 0
        self.INTERVAL = 5

        self.initUI()
        self.initTrack()

    def initUI(self):
        btn = tk.Button(self, text='Back', command=self.back,
                        font=('Arial', 10))
        btn.grid(row=0, column=0)

        tier_roman = self.INT_TO_ROMAN[str(self.tier)]
        self.textVar_minion_goal = tk.StringVar()
        self.textVar_minion_goal.set(
            f'Goal: {self.minion_name} {tier_roman} {self.can_craft}/{self.amount}')
        label = tk.Label(
            self, textvariable=self.textVar_minion_goal, font=('Arial', 20))
        label.grid(row=1, column=1, columnspan=3)

        self.textVar_minion_current = tk.StringVar()
        self.textVar_minion_current.set(
            f'Current: {self.minion_name} {tier_roman}')
        label = tk.Label(self, textvariable=self.textVar_minion_current,
                         font=('Arial', 20))
        label.grid(row=2, column=1, columnspan=3)
        for i in range(1, 12):
            self.img_dict_minion[i] = ImageTk.PhotoImage(Image.open(
                f'./imgs/{self.minion_info["img"]}/{i}.webp').resize((64, 64), Image.ANTIALIAS))
        self.label_minion_img = tk.Label(
            self, image=self.img_dict_minion[self.tier])
        self.label_minion_img.grid(row=3, column=1, rowspan=3)

        for i, item in enumerate(self.item_list):
            item_id = item['item_id']
            item_name = self.ID_TO_NAME[item_id]
            cost = self.LOADER.get_item_value(item_id) * item['required']
            textVar = tk.StringVar()
            textVar.set(f'{item_name} 0.00% (0/{cost})')
            self.textVar_list.append(textVar)
            label = tk.Label(self, textvariable=textVar, font=('Arial', 15))
            label.grid(row=3 + i, column=2)

    def initTrack(self):
        self.used_material = dict()
        self.inventory_minion = self.INVENTORY.count_minion(self.minion)

        for i in range(self.tier, 12):
            if self.inventory_minion[i] > 0:
                self.can_craft = min(self.amount, self.can_craft +
                                     self.inventory_minion[i])
                if self.can_craft == self.amount:
                    self.done()
                    break

        self.track_list = list()
        for i in range(1, self.tier):
            if self.inventory_minion[i] > 0:
                for _ in range(self.inventory_minion):
                    self.track_list.append({'tier': i, 'status': 'original'})
        self.trackNext()

    def trackNext(self):
        ''' get highest tier minion in track_list and upgrade it to highest possible tier
        '''
        self.current_owned = self.track_list.pop()['tier'] if len(
            self.track_list) > 0 else 0
        self.tracking = self.current_owned + 1
        self.current_recipe = self.minion_info['recipe'][str(self.tracking)]
        self.current_item_list = self.current_recipe['item_list']

        flag = False
        cost_list = list()
        for item in self.current_item_list[:-1]:
            item_id = item['item_id']
            variation = self.LOADER.get_collection_variation(item_id)[
                'variation']
            cost = self.LOADER.get_item_value(item_id) * item['required']
            cost_list.append({'variation': variation, 'cost': cost})
            if variation not in self.used_material:
                self.used_material[variation] = 0
            amount = self.INVENTORY.count_item(
                item_id) - self.used_material[variation]

            if amount < cost:
                flag = True
                break

        self.itemB = self.current_item_list[-1]
        self.has_itemB = self.INVENTORY.count_normal_item(
            self.itemB['item_id']) > 0

        if not self.has_itemB:
            flag = True

        if flag:
            self.track()
            return

        for cost in cost_list:
            if cost['variation'] not in self.used_material:
                self.used_material[cost['variation']] = cost['cost']
            else:
                self.used_material[cost['variation']] += cost['cost']

        if self.current_owned == self.tier - 1:
            self.can_craft += 1
            if self.can_craft == self.amount:
                self.done()
                return
        else:
            self.track_list.append(
                {'tier': self.tracking, 'status': 'crafted'})

        self.trackNext()

    def track(self):
        if self.flag:
            tracking = self.current_owned + 1

            self.textVar_minion_current.set(
                f'Current: {self.minion_name} {self.INT_TO_ROMAN[str(tracking)]}')
            self.label_minion_img.configure(
                image=self.img_dict_minion[tracking])

            for i, item in enumerate(self.current_item_list[:-1]):
                cost = self.LOADER.get_item_value(
                    item['item_id']) * item['required']
                variation = self.LOADER.get_collection_variation(
                    item['item_id'])['variation']
                amount = self.INVENTORY.count_item(
                    item['item_id']) - self.used_material[variation]
                self.textVar_list[i].set(
                    f'{item["name"]} {amount/cost:.2%} ({amount}/{cost})')

            if self.current_owned == 0:
                self.textVar_list[-1].set(
                    f'{self.itemB["name"]} {"100.00" if self.has_itemB else "0.00"}% ({1 if self.has_itemB else 0}/1)')
            else:
                self.textVar_list[-1].set(
                    f'{self.itemB["name"]} 100.00% (1/1) ({"owned" if self.has_itemB else "can craft"})')

            self.after(self.INTERVAL * 1000, self.track)

    def done(self):
        self.flag = False
        self.textVar_minion_goal.set('DONE!')
        self.after(3000, self.back)

    def back(self):
        self.flag = False
        self.master.back()
