import math

from d_manager.book import BaseBook
from d_manager.food.stofc2015_food import STOFC2015Food

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


class STOFC2015FoodBook(BaseBook):
    def __init__(self):
        super(STOFC2015FoodBook, self).__init__()
        # ProductFood 用辞書の初期化
        # ID 全体での辞書
        self._foods_by_total_id = dict()
        # 食品毎に内部 ID でも管理する
        for group_id in GROUPS.keys():
            self._foods_by_group[group_id] = dict()

    def append(self, food_id, food):
        """指定したグループにエントリを追加する"""
        if not isinstance(food, STOFC2015Food):
            raise ValueError('Not support type. type={}'.format(type(food)))

        # どのファイルでも共通の食品番号からグループ ID とグループ内の番号を生成する。
        # シート内での食品に付与される索引番号は、食品毎に別々になった Excel ファイルと全ての食品群を一つにまとめたものでは異なる。
        group_id = math.floor(int(food_id) / 1000)
        id_in_group = food_id - group_id * 1000
        self._foods_by_group[group_id][id_in_group] = food

    # def get(self, group_id, id_in_group):
    #     """ID で食品を取得する"""
    #     return self._foods_by_group[group_id][id_in_group]

    def get_by_total_id(self, total_id):
        """食品全体の ID で食品を取得する"""
        total_id = int(total_id)
        group_id = math.floor(total_id / 1000)
        id_in_group = total_id - group_id * 1000
        return self._foods_by_group[group_id][id_in_group]

    # def get_foods(self, group_number):
    #     """指定したグループに登録してある食品の辞書を返す"""
    #     if group_number not in GROUPS.keys():
    #         raise ValueError('Not found group number. number={}'.format(group_number))
    #
    #     return self._foods_by_group[group_number]

    def generator(self):
        for group_id in GROUPS.keys():
            for id_in_group, food in self._foods_by_group[group_id].items():
                # 食品自体ではなく各種 ID も返す
                yield group_id, id_in_group, food
