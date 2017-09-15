import math

from d_manager.book import BaseBook
from d_manager.food.product_food import ProductFood

# 選択可能な食品群
# 日本食品標準成分表 2015 に収載されている食品群を採用
GROUPS = {
    1: '穀類',
    2: 'いも及びでん粉類',
    3: '砂糖及び甘味類',
    4: '豆類',
    5: '種実類',
    6: '野菜類',
    7: '果実類',
    8: 'きのこ類',
    9: '藻類',
    10: '魚介類',
    11: '肉類',
    12: '卵類',
    13: '乳類',
    14: '油脂類',
    15: '菓子類',
    16: 'し好飲料類',
    17: '調味料及び香辛料類',
    18: '調理加工食品類',
}


class ProductFoodBook(BaseBook):
    """市販の食品を収載する Book"""
    def __init__(self):
        super(ProductFoodBook, self).__init__()
        # ProductFood 用辞書の初期化
        # 食品毎に内部 ID で管理している
        for group_id in GROUPS.keys():
            self._foods_by_group[group_id] = dict()

        # 食品群毎に個別の ID で食品を管理している。
        # 食品群内で最大の ID の値を記録しておき、新しい食品の登録時などに使う。
        self._max_id_in_group = dict()
        for group_id in GROUPS.keys():
            self._max_id_in_group[group_id] = 0

    @staticmethod
    def __get_total_id(group_id, id_in_group):
        """グループ ID とグループ内 ID から総合 ID を得る"""
        if group_id not in GROUPS.keys():
            raise ValueError('Not found group number. number={}'.format(group_id))

        return group_id * 1000 + id_in_group

    @staticmethod
    def __get_group_id_and_id_in_group(food_id):
        """食品の総合 ID からグループ ID とグループ内 ID を得る"""
        food_id = int(food_id)
        group_id = math.floor(int(food_id) / 1000)
        if group_id not in GROUPS.keys():
            raise ValueError('Not found group number. number={}'.format(group_id))

        id_in_group = food_id - group_id * 1000
        return group_id, id_in_group

    def append(self, group_id, food):
        """指定したグループに食品情報を追加する"""
        # 市販食品の特徴として、食品群の指定は登録者ができるが、食品の ID は収載されるまで不明である
        # そのため、登録時は食品群の ID のみを登録している
        if group_id not in GROUPS.keys():
            raise ValueError('Not found group number. number={}'.format(group_id))

        if not isinstance(food, ProductFood):
            raise ValueError('Not support type. type={}'.format(type(food)))

        # ID を採番する
        id_in_group = self._max_id_in_group[group_id] + 1
        self._max_id_in_group[group_id] = id_in_group

        self._foods_by_group[group_id][id_in_group] = food

        # 総合 ID を返す
        return self.__get_total_id(group_id, id_in_group)

    def get_by_total_id(self, total_id):
        """総合 ID からエントリを取得する"""
        group_id, id_in_group = self.__get_group_id_and_id_in_group(total_id)
        return self._foods_by_group[group_id][id_in_group]

    def update(self, total_id, food):
        """指定したエントリを更新する"""
        if not isinstance(food, ProductFood):
            raise ValueError('Not support type. type={}'.format(type(food)))

        group_id, id_in_group = self.__get_group_id_and_id_in_group(total_id)
        if id_in_group not in self._foods_by_group[group_id]:
            raise ValueError('Not found. group_id={}, id_in_group={}'.format(group_id, id_in_group))

        orig = self._foods_by_group[group_id][id_in_group]
        self._foods_by_group[group_id][id_in_group] = food
        # 更新前のエントリを返す
        return orig

    def delete(self, total_id):
        """指定したエントリを削除する"""
        group_id, id_in_group = self.__get_group_id_and_id_in_group(total_id)
        if id_in_group not in self._foods_by_group[group_id].keys():
            raise ValueError('Not found. group_id={}, id_in_group={}'.format(group_id, id_in_group))

        c = self._foods_by_group[group_id][id_in_group]
        del self._foods_by_group[group_id][id_in_group]
        # 削除したエントリの参照を返す
        return c

    def generator(self):
        for group_id in GROUPS.keys():
            for id_in_group, food in self._foods_by_group[group_id].items():
                yield group_id, self.__get_total_id(group_id, id_in_group), food

    # def get_foods_by_group(self, group_number):
    #     """指定したグループに登録してある食品の辞書を返す"""
    #     if group_number not in GROUPS.keys():
    #         raise ValueError('Not found group number. number={}'.format(group_number))
    #
    #     return self._foods_by_group[group_number]
