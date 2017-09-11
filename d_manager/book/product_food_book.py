from d_manager.book import BaseBook
from d_manager.food import FOOD_GROUPS
from d_manager.food.product_food import ProductFood


class ProductFoodBook(BaseBook):
    def __init__(self):
        super(ProductFoodBook, self).__init__()
        # ProductFood 用辞書の初期化
        # 食品毎に内部 ID で管理している
        for group_number in FOOD_GROUPS.keys():
            self._entries[group_number] = dict()

        # 食品群毎に個別の ID で食品を管理している。
        # 最大の数を記録しておき、登録時などに使う。
        self._max_id_in_group = dict()
        for group_number in FOOD_GROUPS.keys():
            self._max_id_in_group[group_number] = 0

    def append(self, entry, group_number, id_in_group=None):
        """指定したグループにエントリを追加する"""
        if not isinstance(entry, ProductFood):
            raise ValueError('Not support type. type={}'.format(type(entry)))
        
        if group_number not in FOOD_GROUPS.keys():
            raise ValueError('Not found group number. number={}'.format(group_number))

        # ID を採番する
        if not id_in_group:
            id_in_group = self._max_id_in_group[group_number] + 1
            self._max_id_in_group[group_number] = id_in_group
        else:
            # グループ内の ID が指定されていたら、最大値より大きい整数であることを確認してから採用する。
            id_in_group = int(id_in_group)
            if id_in_group <= self._max_id_in_group[group_number]:
                raise ValueError('Invalid id in group. id={}'.format(id_in_group))
            else:
                self._max_id_in_group[group_number] = id_in_group

        self._entries[group_number][id_in_group] = entry
        # 採番した ID を返す
        return id_in_group

    def get_entries_by_group(self, group_number):
        """指定したグループに登録してある食品の辞書を返す"""
        if group_number not in FOOD_GROUPS.keys():
            raise ValueError('Not found group number. number={}'.format(group_number))

        return self._entries[group_number]
        
    def update(self, group_number, id_in_group, entry):
        """指定したエントリを更新する"""
        if not isinstance(entry, ProductFood):
            raise ValueError('Not support type. type={}'.format(type(entry)))

        if id_in_group not in self._entries[group_number]:
            raise ValueError('Not found id in the group. group={}, id_in_group={}'.format(group_number, id_in_group))

        orig = self._entries[group_number][id_in_group]
        self._entries[group_number][id_in_group] = entry
        # 更新前のエントリを返す
        return orig

    def delete(self, group_number, id_in_group):
        """指定したエントリを削除する"""
        if id_in_group not in self._entries[group_number]:
            raise ValueError('Not found id in the group. group={}, id_in_group={}'.format(group_number, id_in_group))

        # 削除したエントリの参照を返す
        c = self._entries[group_number][id_in_group]
        del self._entries[group_number][id_in_group]
        return c
