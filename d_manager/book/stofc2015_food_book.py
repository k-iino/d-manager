from d_manager.book import BaseBook
from d_manager.food import FOOD_GROUPS
from d_manager.food.stofc2015_food import STOFC2015Food


class STOFC2015FoodBook(BaseBook):
    def __init__(self):
        super(STOFC2015FoodBook, self).__init__()
        # ProductFood 用辞書の初期化
        # 食品毎に内部 ID で管理している
        for group_number in FOOD_GROUPS.keys():
            self._entries[group_number] = dict()

    def append(self, entry, group_number, id_in_group):
        """指定したグループにエントリを追加する"""
        if not isinstance(entry, STOFC2015Food):
            raise ValueError('Not support type. type={}'.format(type(entry)))

        if group_number not in FOOD_GROUPS.keys():
            raise ValueError('Not found group number. number={}'.format(group_number))

        self._entries[group_number][id_in_group] = entry

    def get_entries_by_group(self, group_number):
        """指定したグループに登録してある食品の辞書を返す"""
        if group_number not in FOOD_GROUPS.keys():
            raise ValueError('Not found group number. number={}'.format(group_number))

        return self._entries[group_number]

    def generator(self):
        for group_num in FOOD_GROUPS.keys():
            for food in self._entries[group_num].values():
                yield food
